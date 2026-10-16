import os
import shutil
import subprocess
from typing import List, Optional
from schemas.contracts import MasterScript, AudioManifest, SceneAudioAsset, WordTimestamp

class DatAudioEngineer:
    """Agent Đạt - Kỹ sư Âm thanh & Lồng tiếng (Voiceover) sử dụng VieNeu-TTS Studio."""

    def __init__(
        self,
        output_dir: str = "./storage/audio",
        vieneu_url: str = "http://127.0.0.1:7860/",
        default_voice: str = "Trúc Ly"
    ):
        self.output_dir = output_dir
        self.vieneu_url = vieneu_url.rstrip("/") + "/"
        self.default_voice = default_voice
        os.makedirs(self.output_dir, exist_ok=True)
        self._vieneu_client = None

    def _get_client(self):
        if self._vieneu_client is None:
            try:
                from gradio_client import Client
                self._vieneu_client = Client(self.vieneu_url)
                # Tự động nạp model VieNeu-TTS nếu chưa nạp
                try:
                    self._vieneu_client.predict(
                        'VieNeu-TTS-v3-Nano (preview)',
                        'VieNeu-Codec',
                        'Auto',
                        False,
                        '',
                        'VieNeu-TTS-v3-Nano (preview)',
                        '',
                        api_name='/load_model'
                    )
                except Exception as ex:
                    print(f"[Đạt - Audio] Lưu ý load_model: {ex}")
            except Exception as e:
                print(f"[Đạt - Audio] Chưa kết nối được VieNeu-TTS tại {self.vieneu_url}: {e}. Sẽ dùng fallback.")
                self._vieneu_client = None
        return self._vieneu_client

    def measure_duration_ms(self, audio_path: str) -> int:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
            return int(float(res.stdout.strip()) * 1000)
        except Exception:
            return 4000

    def synthesize_with_vieneu(self, text: str, output_wav_path: str, voice_name: Optional[str] = None) -> bool:
        """Gọi Gradio API của VieNeu-TTS để tạo giọng đọc chất lượng cao."""
        client = self._get_client()
        if not client:
            return False

        voice = voice_name or self.default_voice
        try:
            res = client.predict(
                text,
                voice,
                None,  # audio_sample
                "",    # prompt_text
                "Standard (Một lần)",
                True,  # batch_processing
                2,     # batch_size
                0.8,   # temperature
                256,   # max_chars
                False, # denoise
                api_name="/wrapper",
            )
            generated_audio = res[0]
            if generated_audio and os.path.exists(generated_audio):
                shutil.copy2(generated_audio, output_wav_path)
                return True
            return False
        except Exception as e:
            print(f"[Đạt - VieNeu-TTS] Thất bại khi đọc: '{text[:30]}...': {e}")
            return False

    def generate_fallback_silence(self, duration_sec: float, output_wav: str):
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(duration_sec),
            "-q:a", "9",
            output_wav
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def process_script(self, master_script: MasterScript, project_id: str) -> AudioManifest:
        proj_audio_dir = os.path.join(self.output_dir, project_id)
        os.makedirs(proj_audio_dir, exist_ok=True)
        
        scene_audios: List[SceneAudioAsset] = []
        total_duration = 0

        for scene in master_script.scenes:
            audio_file = os.path.join(proj_audio_dir, f"{scene.scene_id}.wav")
            
            # 1. Thử gọi VieNeu-TTS
            success = self.synthesize_with_vieneu(scene.spoken_text, audio_file)
            
            # 2. Nếu VieNeu-TTS chưa bật hoặc lỗi, fallback tính toán thời lượng ước tính
            if not success or not os.path.exists(audio_file):
                words = scene.spoken_text.split()
                est_duration_sec = max(3.0, len(words) / 3.0)
                self.generate_fallback_silence(est_duration_sec, audio_file)

            dur_ms = self.measure_duration_ms(audio_file)
            total_duration += dur_ms

            # Tạo word timestamps
            words = scene.spoken_text.split()
            word_ts = []
            cur_ms = 0
            step_ms = int(dur_ms / max(1, len(words)))
            for w in words:
                word_ts.append(WordTimestamp(word=w, start_ms=cur_ms, end_ms=cur_ms + step_ms))
                cur_ms += step_ms

            scene_audios.append(SceneAudioAsset(
                scene_id=scene.scene_id,
                audio_filepath=audio_file,
                actual_duration_ms=dur_ms,
                word_timestamps=word_ts,
                sfx_cue="whoosh" if scene.section_type in ["HOOK", "MINI_HOOK"] else None
            ))

        bgm_path = "./assets/bgm/cinematic_neutral.mp3"
        return AudioManifest(
            background_music_filepath=bgm_path,
            bgm_mood="investigative_documentary",
            total_audio_duration_ms=total_duration,
            scene_audios=scene_audios
        )
