"""
Modern sidebar calculator: digits, operators, memory, percent, +/- and safe evaluation.
Returns the current display value so `app.py` can use it.
"""

import ast
import re
import streamlit as st


# Streamlit fragment support (optional)
try:
    from streamlit import fragment
except ImportError:
    def fragment(func):
        return func


CALCULATOR_STYLE = """
<style>
[data-testid='stSidebar'] .stButton,
[data-testid='stSidebar'] .stButton>button,
[data-testid='stSidebar'] button {
    min-width: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    font-size: 0.92rem !important;
    padding: 0.45rem 0.55rem !important;
    white-space: nowrap !important;
    box-sizing: border-box !important;
}

[data-testid='stSidebar'] .stButton {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 0 !important;
}

[data-testid='stSidebar'] .stButton>button {
    width: 100% !important;
}

</style>
"""


def _safe_eval(expr):
    node = ast.parse(expr, mode="eval")

    def _eval(node):

        if isinstance(node, ast.Expression):
            return _eval(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant")

        if hasattr(ast, "Num") and isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            val = _eval(node.operand)
            return +val if isinstance(node.op, ast.UAdd) else -val

        if isinstance(node, ast.BinOp):

            left = _eval(node.left)
            right = _eval(node.right)

            if isinstance(node.op, ast.Add):
                return left + right

            if isinstance(node.op, ast.Sub):
                return left - right

            if isinstance(node.op, ast.Mult):
                return left * right

            if isinstance(node.op, ast.Div):
                return left / right

            if isinstance(node.op, ast.Pow):
                return left ** right

            if isinstance(node.op, ast.Mod):
                return left % right

        raise ValueError("Unsupported expression")

    return _eval(node)


def evaluate_expression(raw_expression):

    if raw_expression is None:
        raise ValueError("No expression provided")

    expression = str(raw_expression)

    cleaned = "".join(
        ch for ch in expression
        if ch in "0123456789.+-*/() %"
    )

    cleaned = cleaned.replace("%", "/100")

    while cleaned and cleaned[-1] in "+-*/. %":
        cleaned = cleaned[:-1]

    if not cleaned:
        raise ValueError("Empty expression")

    result = _safe_eval(cleaned)

    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return result, cleaned




def render_calculator():

    if "calc_display" not in st.session_state:
        st.session_state.calc_display = ""

    if "calc_mem" not in st.session_state:
        st.session_state.calc_mem = 0.0


    st.sidebar.markdown(
        CALCULATOR_STYLE,
        unsafe_allow_html=True
    )

    st.sidebar.header("Αριθμομηχανή")

    st.sidebar.markdown(
        f"### `{st.session_state.calc_display or '0'}`"
    )


    def get():
        return st.session_state.calc_display


    def set_value(value):
        st.session_state.calc_display = value


    def clear_calc():
        set_value("")


    def delete_calc():
        set_value(get()[:-1])


    def append_digit(d):

        cur = get()

        if cur in ("", "ERR"):
            set_value("0." if d == "." else d)
            return

        if cur == "0" and d != ".":
            set_value(d)
            return

        set_value(cur + d)


    def append_dot():

        cur = get()

        parts = re.split(r'([+\-*/])', cur)

        if "." in parts[-1]:
            return

        set_value(cur + "." if cur else "0.")


    def append_operator(op):

        cur = get()

        if not cur:
            if op == "-":
                set_value("-")
            return

        if cur[-1] in "+-*/":
            set_value(cur[:-1] + op)
        else:
            set_value(cur + op)


    def toggle_sign():

        cur = get()

        if not cur or cur == "ERR":
            return

        parts = re.split(r'([+\-*/])', cur)

        last = parts[-1]

        if last.startswith("-"):
            last = last[1:]
        else:
            last = "-" + last

        parts[-1] = last

        set_value("".join(parts))


    def percent():

        cur = get()

        if not cur:
            return

        parts = re.split(r'([+\-*/])', cur)

        try:
            parts[-1] = str(float(parts[-1]) / 100)
        except:
            return

        set_value("".join(parts))


    def mem_clear():
        st.session_state.calc_mem = 0.0


    def mem_recall():
        set_value(str(st.session_state.calc_mem))


    def mem_add():

        try:
            st.session_state.calc_mem += float(get())
        except:
            pass


    def mem_sub():

        try:
            st.session_state.calc_mem -= float(get())
        except:
            pass


    def calculate():

        try:

            result, cleaned = evaluate_expression(get())

            if "calc_history" not in st.session_state:
                st.session_state.calc_history = []

            st.session_state.calc_history.append(
                {
                    "raw": get(),
                    "cleaned": cleaned,
                    "result": str(result)
                }
            )

            set_value(str(result))

        except Exception:

            set_value("ERR")


    # Buttons

    rows = [

        [("MC", mem_clear), ("MR", mem_recall), ("M+", mem_add), ("M-", mem_sub)],
        [("C", clear_calc), ("DEL", delete_calc), ("%", percent), ("/", lambda: append_operator("/"))],
        [("7", lambda: append_digit("7")), ("8", lambda: append_digit("8")), ("9", lambda: append_digit("9")), ("*", lambda: append_operator("*"))],
        [("4", lambda: append_digit("4")), ("5", lambda: append_digit("5")), ("6", lambda: append_digit("6")), ("-", lambda: append_operator("-"))],
        [("1", lambda: append_digit("1")), ("2", lambda: append_digit("2")), ("3", lambda: append_digit("3")), ("+", lambda: append_operator("+"))],
        [("+/-", toggle_sign), ("0", lambda: append_digit("0")), (".", append_dot), ("=", calculate)]
    ]


    for row in rows:

        cols = st.sidebar.columns(4)

        for col, (text, func) in zip(cols, row):
            col.button(
                text,
                on_click=func,
                use_container_width=True
            )


    return st.session_state.get(
        "calc_display",
        ""
    )