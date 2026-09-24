from avyra.core.core import AVYRACore


def main() -> None:
    avyra = AVYRACore()

    print("=" * 50)
    print("AVYRA Core v0.1")
    print("Adaptive Voice, Yielding Reasoning & Automation")
    print("=" * 50)
    print("Type 'exit' to stop AVYRA.\n")

    while True:
        try:
            user_input = input("You > ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("AVYRA > Shutting down.")
                break

            response = avyra.handle(user_input)

            print(f"AVYRA > {response.text}")
            print(
                f"        [intent={response.metadata['intent']} "
                f"language={response.metadata['language']}]\n"
            )

        except (KeyboardInterrupt, EOFError):
            print("\nAVYRA > Shutting down.")
            break

        except Exception as exc:
            print(f"AVYRA ERROR > {exc}")


if __name__ == "__main__":
    main()