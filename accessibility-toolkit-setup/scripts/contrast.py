#!/usr/bin/env python3
"""Calculate contrast for two opaque six-digit sRGB hex colors."""
import argparse
import json
import re


def luminance(value: str) -> float:
    """Return relative luminance, rejecting CSS expressions and alpha colors."""
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise ValueError('Expected an opaque six-digit color such as #105289')
    channels = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4
              for x in channels]
    return sum(x * weight for x, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(foreground: str, background: str) -> float:
    """Return the symmetric WCAG contrast ratio for the supplied opaque pair."""
    low, high = sorted((luminance(foreground), luminance(background)))
    return (high + .05) / (low + .05)


def main() -> None:
    """Print a ratio; the caller chooses the applicable text/graphics threshold."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--foreground', required=True)
    parser.add_argument('-b', '--background', required=True)
    args = parser.parse_args()
    try:
        ratio = contrast(args.foreground, args.background)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps({'foreground': args.foreground, 'background': args.background,
                      'contrast_ratio': round(ratio, 6)}))


if __name__ == '__main__':
    main()
