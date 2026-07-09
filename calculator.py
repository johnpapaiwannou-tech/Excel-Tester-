"""
Modern sidebar calculator: digits, operators, memory, percent, +/- and safe evaluation.
Returns the current display value so `app.py` can use it.
"""
import ast
import re
import streamlit as st


def _safe_eval(expr):
    node = ast.parse(expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant")
        # For Python <3.8 compatibility
        if hasattr(ast, 'Num') and isinstance(node, ast.Num):
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


def evaluate_expression(raw_expression: str):
    """Public API: evaluate a raw expression string.

    Returns tuple (result, cleaned_expression) or raises Exception on parse/eval error.
    """
    if raw_expression is None:
        raise ValueError("No expression provided")
    expression = str(raw_expression)
    # Keep allowed chars and percent sign
    cleaned = "".join(ch for ch in expression if ch in "0123456789.+-*/() %")
    # Replace percent characters with division by 100 as a simple support
    cleaned = cleaned.replace('%', '/100')
    # Strip trailing operators/dots/spaces
    while cleaned and cleaned[-1] in "+-*/. %":
        cleaned = cleaned[:-1]
    if not cleaned:
        raise ValueError("Expression is empty after cleaning")
    result = _safe_eval(cleaned)
    # Normalize integer floats
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return result, cleaned


def render_calculator():
    if "calc_display" not in st.session_state:
        st.session_state.calc_display = ""
    if "calc_mem" not in st.session_state:
        st.session_state.calc_mem = 0.0

    st.sidebar.header("Αριθμομηχανή")
    st.sidebar.markdown(f"### `{st.session_state.calc_display or '0'}`")
    st.sidebar.markdown(
        """
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
        [data-testid='stSidebar'] .css-1lcbmhc.e1fqkh3o3 {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 6px !important;
        }
        @media (max-width: 540px) {
            [data-testid='stSidebar'] .css-1lcbmhc.e1fqkh3o3 {
                grid-template-columns: repeat(2, 1fr) !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def _get():
        return st.session_state.calc_display

    def _set(v):
        st.session_state.calc_display = v

    def clear_calc():
        _set("")

    def delete_calc():
        cur = _get()
        _set(cur[:-1])

    def _append_digit(d):
        cur = _get()
        if cur in ("", "ERR"):
            _set(d if d != "." else "0.")
            return
        if cur == "0" and d != ".":
            _set(d)
            return
        # Append digit
        _set(cur + d)

    def _append_dot():
        cur = _get()
        parts = re.split(r'([+\-*/])', cur)
        last = parts[-1]
        if "." in last:
            return
        if last == "":
            _set(cur + "0.")
        else:
            _set(cur + ".")

    def _append_op(op):
        cur = _get()
        if cur in ("", "ERR"):
            if op == "-":
                _set("-")
            return
        if cur[-1] in "+-*/":
            # replace last operator (allow minus after operator for negative)
            if op == "-" and cur[-1] != "-":
                _set(cur + op)
            else:
                _set(cur[:-1] + op)
            return
        _set(cur + op)

    def toggle_sign():
        cur = _get()
        if not cur or cur == "ERR":
            return
        # Toggle sign of last number
        parts = re.split(r'([+\-*/])', cur)
        last = parts[-1]
        if last == "":
            return
        if last.startswith("-"):
            last = last[1:]
        else:
            last = "-" + last
        parts[-1] = last
        _set(''.join(parts))

    def percent():
        cur = _get()
        if not cur or cur == "ERR":
            return
        parts = re.split(r'([+\-*/])', cur)
        last = parts[-1]
        try:
            val = float(last)
        except Exception:
            return
        val = val / 100.0
        parts[-1] = str(val)
        _set(''.join(parts))

    def mem_clear():
        st.session_state.calc_mem = 0.0

    def mem_recall():
        _set(str(st.session_state.calc_mem))

    def mem_add():
        try:
            st.session_state.calc_mem += float(_get())
        except Exception:
            pass

    def mem_sub():
        try:
            st.session_state.calc_mem -= float(_get())
        except Exception:
            pass

    def calculate_result():
        expression = _get()
        try:
            result, cleaned = evaluate_expression(expression)
            # append to history
            if "calc_history" not in st.session_state:
                st.session_state.calc_history = []
            st.session_state.calc_history.append({
                "raw": expression,
                "cleaned": cleaned,
                "result": str(result),
            })
            st.session_state.calc_result = result
            st.session_state.calc_error = ""
            _set(str(result))
        except Exception as e:
            st.session_state.calc_result = ""
            st.session_state.calc_error = str(e)
            st.sidebar.error(f"Calculator error: {e}")
            st.sidebar.write(f"raw: {expression}")
            st.sidebar.write(f"error: {e}")
            _set("ERR")

    # Layout
    r1, r2, r3, r4 = st.sidebar.columns(4)
    r1.button("MC", on_click=mem_clear)
    r2.button("MR", on_click=mem_recall)
    r3.button("M+", on_click=mem_add)
    r4.button("M-", on_click=mem_sub)

    r1, r2, r3, r4 = st.sidebar.columns(4)
    r1.button("C", on_click=clear_calc)
    r2.button("DEL", on_click=delete_calc)
    r3.button("%", on_click=percent)
    r4.button("/", on_click=_append_op, args=("/",))

    r1, r2, r3, r4 = st.sidebar.columns(4)
    r1.button("7", on_click=_append_digit, args=("7",))
    r2.button("8", on_click=_append_digit, args=("8",))
    r3.button("9", on_click=_append_digit, args=("9",))
    r4.button("*", on_click=_append_op, args=("*",))

    r1, r2, r3, r4 = st.sidebar.columns(4)
    r1.button("4", on_click=_append_digit, args=("4",))
    r2.button("5", on_click=_append_digit, args=("5",))
    r3.button("6", on_click=_append_digit, args=("6",))
    r4.button("-", on_click=_append_op, args=("-",))

    r1, r2, r3, r4 = st.sidebar.columns(4)
    r1.button("1", on_click=_append_digit, args=("1",))
    r2.button("2", on_click=_append_digit, args=("2",))
    r3.button("3", on_click=_append_digit, args=("3",))
    r4.button("+", on_click=_append_op, args=("+",))

    r1, r2, r3, r4 = st.sidebar.columns(4)
    r1.button("+/-", on_click=toggle_sign)
    r2.button("0", on_click=_append_digit, args=("0",))
    r3.button(".", on_click=_append_dot)
    r4.button("=", on_click=calculate_result)

    return st.session_state.get("calc_display", "")