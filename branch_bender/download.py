__resources__ = {"README.md": "README.md"}


from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, commit
from exercise_utils.gitmastery import create_start_tag


def setup(verbose: bool = False):
    create_start_tag(verbose)

    # feature/login branch
    checkout("feature/login", True, verbose)
    create_or_update_file(
        "src/login.js",
        """
        function login(username, password) {
            return username === "admin" && password == "admin"
        }


        """,
    )
    add(["src/login.js"], verbose)
    commit("Add login script", verbose)

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
    add(["login.html"], verbose)
    commit("Add login page", verbose)

    checkout("main", False, verbose)

    # feature/dashboard branch
    checkout("feature/dashboard", True, verbose)

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
    add(["dashboard.html"], verbose)
    commit("Add dashboard header", verbose)

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
    add(["dashboard.html"], verbose)
    commit("Add dashboard body", verbose)

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
    add(["dashboard.html"], verbose)
    commit("Add dashboard footer", verbose)

    checkout("main", False, verbose)

    # feature/payments branch
    checkout("feature/payments", True, verbose)

    create_or_update_file(
        "src/payments.js",
        """
        function processPayment(cardNumber, amount) {
            // Simulated payment logic
            return `Charged $${amount} to card ending in ${cardNumber.slice(-4)}`;
        }
        """,
    )
    add(["src/payments.js"], verbose)
    commit("Add payments script", verbose)

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
    add(["payments.html"], verbose)
    commit("Add payments page", verbose)

    checkout("main", False, verbose)
