import os
import textwrap
import pathlib
import subprocess
from sys import exit
from typing import List, Optional

__resources__ = {"README.md": "README.md"}


def run_command(command: List[str], verbose: bool) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        if verbose:
            print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        if verbose:
            print(e.stderr)
        exit(1)


def create_or_update_file(
    filepath: str | pathlib.Path, contents: Optional[str] = None
) -> None:
    if os.path.dirname(filepath) != "":
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if contents is None:
        open(filepath, "a").close()
    else:
        with open(filepath, "w") as file:
            file.write(textwrap.dedent(contents).lstrip())


def setup(verbose: bool = False):
    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split("\n")[0]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)

    # feature/login branch
    run_command(["git", "checkout", "-b", "feature/login"], verbose)
    create_or_update_file(
        "src/login.js",
        """
        function login(username, password) {
            return username === "admin" && password == "admin"
        }
        """,
    )
    run_command(["git", "add", "src/login.js"], verbose)
    run_command(["git", "commit", "-m", "Add login script"], verbose)

    create_or_update_file(
        "login.html",
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
            <script src="src/login.js"></script>
        </head>
        <body>
            <h1>Login</h1>
            <form onsubmit="handleLogin(event)">
                <input type="text" id="username" placeholder="Username" />
                <input type="password" id="password" placeholder="Password" />
                <button type="submit">Login</button>
            </form>
            <script>
                function handleLogin(event) {
                    event.preventDefault();
                    const user = document.getElementById('username').value;
                    const pass = document.getElementById('password').value;
                    alert(login(user, pass) ? "Welcome!" : "Access Denied");
                }
            </script>
        </body>
        </html>
        """,
    )
    run_command(["git", "add", "login.html"], verbose)
    run_command(["git", "commit", "-m", "Add login page"], verbose)

    run_command(["git", "checkout", "main"], verbose)

    # feature/dashboard branch
    run_command(["git", "checkout", "-b", "feature/dashboard"], verbose)

    create_or_update_file(
        "dashboard.html",
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <header>
                <h1>User Dashboard</h1>
            </header>
        </body>
        </html>
        """,
    )
    run_command(["git", "add", "dashboard.html"], verbose)
    run_command(["git", "commit", "-m", "Add dashboard header"], verbose)

    create_or_update_file(
        "dashboard.html",
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <header>
                <h1>User Dashboard</h1>
            </header>
            <main>
                <p>Welcome back, user!</p>
                <p>Your account is in good standing.</p>
            </main>
        </body>
        </html>
        """,
    )
    run_command(["git", "add", "dashboard.html"], verbose)
    run_command(["git", "commit", "-m", "Add dashboard body"], verbose)

    create_or_update_file(
        "dashboard.html",
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <header>
                <h1>User Dashboard</h1>
            </header>
            <main>
                <p>Welcome back, user!</p>
                <p>Your account is in good standing.</p>
            </main>
            <footer>
                <small>Copyright (c) 2025 Acme Corp</small>
            </footer>
        </body>
        </html>
        """,
    )
    run_command(["git", "add", "dashboard.html"], verbose)
    run_command(["git", "commit", "-m", "Add dashboard footer"], verbose)

    run_command(["git", "checkout", "main"], verbose)

    # feature/payments branch
    run_command(["git", "checkout", "-b", "feature/payments"], verbose)

    create_or_update_file(
        "src/payments.js",
        """
        function processPayment(cardNumber, amount) {
            // Simulated payment logic
            return `Charged $${amount} to card ending in ${cardNumber.slice(-4)}`;
        }
        """,
    )
    run_command(["git", "add", "src/payments.js"], verbose)
    run_command(["git", "commit", "-m", "Add payments script"], verbose)

    create_or_update_file(
        "payments.html",
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Payments</title>
            <script src="src/payments.js"></script>
        </head>
        <body>
            <h1>Make a Payment</h1>
            <form onsubmit="handlePayment(event)">
                <input type="text" id="cardNumber" placeholder="Card Number" />
                <input type="number" id="amount" placeholder="Amount" />
                <button type="submit">Pay</button>
            </form>
            <script>
                function handlePayment(event) {
                    event.preventDefault();
                    const card = document.getElementById('cardNumber').value;
                    const amount = document.getElementById('amount').value;
                    alert(processPayment(card, amount));
                }
            </script>
        </body>
        </html>
        """,
    )
    run_command(["git", "add", "payments.html"], verbose)
    run_command(["git", "commit", "-m", "Add payments page"], verbose)

    run_command(["git", "checkout", "main"], verbose)
