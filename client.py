import argparse
import sys
import tkinter as tk
import urllib.error

from api_client import EchoSounderClient
from profile_plot import plot_profile
from route import process_route


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Клієнт сервера ехолота")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Базова URL-адреса API",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Кількість запитів для накопичення одного кроку",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Обмежити кількість оброблених кроків для перевірки",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Не відкривати візуальний графік",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.repeats < 1:
        print("Помилка: --repeats має бути не менше 1", file=sys.stderr)
        return 2
    if args.max_steps is not None and args.max_steps < 1:
        print("Помилка: --max-steps має бути не менше 1", file=sys.stderr)
        return 2

    try:
        client = EchoSounderClient(args.base_url)
        config = client.get_config()
        pulse = client.get_pulse()
        route_depths, max_depth = process_route(
            client,
            config,
            pulse,
            args.repeats,
            args.max_steps,
        )
    except (urllib.error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
        print(f"Помилка клієнта: {exc}", file=sys.stderr)
        return 1

    print(
        f"\nМаксимальна глибина вимірювання системи: "
        f"{max_depth:.3f} м"
    )

    if not args.no_plot:
        try:
            plot_profile(route_depths, max_depth, accumulated=True)
        except tk.TclError as exc:
            print(f"Візуалізацію неможливо відкрити: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
