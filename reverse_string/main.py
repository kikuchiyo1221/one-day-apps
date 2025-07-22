#!/usr/bin/env python3
import argparse


def reverse(text: str) -> str:
    """文字列を反転して返す"""
    return text[::-1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Reverse a given string.")
    parser.add_argument("text", help="Text to reverse")
    args = parser.parse_args()

    print(reverse(args.text))


if __name__ == "__main__":
    main() 