import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from flow import BlogFlow  # noqa: E402
from exporters import SUPPORTED_FORMATS  # noqa: E402



def main() -> None:
    p = argparse.ArgumentParser(description="Autonomous blog-writing Flow (CrewAI + Ollama)")
    p.add_argument("--topic", required=True, help="Blog topic")
    p.add_argument("--audience", default="general readers")
    p.add_argument("--tone", default="conversational and informative")
    p.add_argument("--words", type=int, default=900, help="Target word count")
    p.add_argument("--format", default="markdown", choices=SUPPORTED_FORMATS + ["md"],
                   help="Output file format")
    p.add_argument("--output-dir", default="output")
    p.add_argument("--plot", action="store_true", help="Save a flow diagram (flow.html) and exit")
    args = p.parse_args()

    flow = BlogFlow()
    if args.plot:
        flow.plot("blog_flow")
        return

    result = flow.kickoff(inputs={
        "topic": args.topic,
        "audience": args.audience,
        "tone": args.tone,
        "word_count": args.words,
        "output_format": args.format,
        "output_dir": args.output_dir,
    })
    print(f"\nDone -> {result}")


if __name__ == "__main__":
    main()