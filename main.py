from pyscript import document, when

# Proposed CampusPrint Hub prices
PRICES = {
    "bw": 2,
    "color": 5,
    "copy": 2,
    "scan": 5,
    "format": 10,
    "binding": 25,
}

SERVICE_NAMES = {
    "bw": "Black-and-white printing",
    "color": "Colored printing",
    "copy": "Photocopying",
    "scan": "Document scanning",
    "format": "Document formatting",
    "binding": "Binding",
}

UNIT_NAMES = {
    "bw": "pages",
    "color": "pages",
    "copy": "pages",
    "scan": "files",
    "format": "files",
    "binding": "binding service(s)",
}


def get_element(element_id):
    return document.querySelector(f"#{element_id}")


def calculate_total():
    service = get_element("service").value
    quantity_text = get_element("quantity").value

    try:
        quantity = int(quantity_text)
    except (ValueError, TypeError):
        raise ValueError("Please enter a valid whole number.")

    if quantity < 1 or quantity > 1000:
        raise ValueError("Quantity must be between 1 and 1000.")

    total = PRICES[service] * quantity

    # Rush service adds ₱5 once per order.
    if get_element("rush").checked:
        total += 5

    return service, quantity, total


def show_message(message, success=True):
    box = get_element("order-message")
    box.textContent = message
    box.className = (
        "message visible success"
        if success
        else "message visible error"
    )


def update_estimate():
    try:
        service, quantity, total = calculate_total()

        get_element("total-price").textContent = f"₱{total:.2f}"

        note = (
            f"{quantity} {UNIT_NAMES[service]} × "
            f"₱{PRICES[service]:.2f}"
        )

        if get_element("rush").checked:
            note += " + ₱5.00 rush fee"

        get_element("estimate-note").textContent = (
            note + ". Final price may vary for formatting and binding."
        )

        return True

    except (ValueError, KeyError) as error:
        get_element("total-price").textContent = "—"
        get_element("estimate-note").textContent = str(error)
        return False
      
