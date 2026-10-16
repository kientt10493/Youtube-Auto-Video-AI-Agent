import sys
import os

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Đảm bảo ffmpeg và ffprobe luôn có sẵn trong PATH
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from agents.minh_orchestrator import MinhOrchestrator

def main():
    topic = "Vì sao đồng hồ Rolex đắt đỏ nhưng ai cũng khao khát sở hữu?"
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])

    print(f"Bắt đầu chạy thử nghiệm Pipeline với chủ đề: '{topic}'")
    orchestrator = MinhOrchestrator(max_qa_retries=2)
    result = orchestrator.run_full_pipeline(topic)

    print("\n================== KẾT QUẢ THỬ NGHIỆM THÀNH CÔNG ==================")
    print(f"Project ID: {result['project_id']}")
    print(f"Tiêu đề A/B: {result['publish_package']['ab_test_titles']}")
    print(f"Video file: {result['final_video_path']}")
    print("===================================================================")

if __name__ == "__main__":
    main()
