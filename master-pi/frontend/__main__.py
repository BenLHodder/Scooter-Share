from app import ScooterWebApp


def main():
    """Start the Web Application"""

    app = ScooterWebApp()
    app.run(debug=True, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
