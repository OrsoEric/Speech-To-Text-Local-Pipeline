from pathlib import Path
from collections import Counter
import json


C_S_PROFILE = Path(
    "onnxruntime_profile__2026-08-22_12-46-13_165.json"
)

C_S_LOG_FILE = Path(
    "onnx_profile_event_analysis.log"
)


def log(file, text=""):
    print(text)
    file.write(text + "\n")


def main():
    with C_S_PROFILE.open("r", encoding="utf-8") as f:
        events = json.load(f)

    with C_S_LOG_FILE.open(
        "w",
        encoding="utf-8",
    ) as log_file:

        log(log_file, f"Profile: {C_S_PROFILE}")
        log(log_file, f"Total events: {len(events)}")
        log(log_file)

        # ---------------------------------------------------------
        # Event names
        # ---------------------------------------------------------

        name_counts = Counter(
            event.get("name", "<NO NAME>")
            for event in events
        )

        log(log_file, "=" * 80)
        log(log_file, "EVENT NAMES")
        log(log_file, "=" * 80)

        for name, count in name_counts.most_common():
            log(
                log_file,
                f"{count:6d}  {name}",
            )

        # ---------------------------------------------------------
        # Categories
        # ---------------------------------------------------------

        category_counts = Counter(
            event.get("cat", "<NO CATEGORY>")
            for event in events
        )

        log(log_file)
        log(log_file, "=" * 80)
        log(log_file, "EVENT CATEGORIES")
        log(log_file, "=" * 80)

        for category, count in category_counts.most_common():
            log(
                log_file,
                f"{count:6d}  {category}",
            )

        # ---------------------------------------------------------
        # Events containing explicit transfer/synchronization
        # terms IN THE EVENT NAME ONLY
        # ---------------------------------------------------------

        transfer_terms = (
            "memcpy",
            "mem_copy",
            "copy",
            "transfer",
            "upload",
            "download",
            "sync",
            "wait",
            "fence",
        )

        matching_events = []

        for event in events:
            name = str(
                event.get("name", "")
            ).lower()

            if any(
                term in name
                for term in transfer_terms
            ):
                matching_events.append(event)

        log(log_file)
        log(log_file, "=" * 80)
        log(
            log_file,
            "TRANSFER / SYNCHRONIZATION EVENTS",
        )
        log(log_file, "=" * 80)

        log(
            log_file,
            f"Matching events: {len(matching_events)}",
        )
        log(log_file)

        for event in matching_events:
            log(
                log_file,
                f"{event.get('dur', 0) / 1000:12.3f} ms  "
                f"{event.get('name', '')}",
            )

            log(
                log_file,
                f"    category: {event.get('cat')}",
            )

            log(
                log_file,
                f"    args: {event.get('args', {})}",
            )

            log(log_file)

        # ---------------------------------------------------------
        # Longest events
        # ---------------------------------------------------------

        duration_events = [
            event
            for event in events
            if event.get("ph") == "X"
            and event.get("dur", 0) > 0
        ]

        duration_events.sort(
            key=lambda event: event.get("dur", 0),
            reverse=True,
        )

        log(log_file)
        log(log_file, "=" * 80)
        log(log_file, "TOP 100 LONGEST EVENTS")
        log(log_file, "=" * 80)

        for index, event in enumerate(
            duration_events[:100],
            start=1,
        ):
            log(
                log_file,
                f"{index:3d}. "
                f"{event.get('dur', 0) / 1000:12.3f} ms  "
                f"{event.get('name', '')}",
            )

            log(
                log_file,
                f"     category: {event.get('cat')}",
            )

            log(
                log_file,
                f"     args: {event.get('args', {})}",
            )

            log(log_file)

    print()
    print(
        f"Log written to: "
        f"{C_S_LOG_FILE.resolve()}"
    )


if __name__ == "__main__":
    main()