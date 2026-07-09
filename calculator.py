import streamlit as st
import streamlit.components.v1 as components


def render_calculator():

    st.sidebar.header("Αριθμομηχανή")

    components.html(
        """
        <style>
        .calc {
            width: 260px;
            background: rgba(255,255,255,0.15);
            padding: 15px;
            border-radius: 20px;
        }

        .display {
            width: 100%;
            height: 45px;
            font-size: 22px;
            text-align: right;
            border-radius: 10px;
            margin-bottom: 10px;
            border: none;
            padding: 5px;
        }

        button {
            width: 55px;
            height: 45px;
            margin: 3px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            font-size:16px;
        }

        </style>


        <div class="calc">

            <input id="display" class="display" value="">

            <br>

            <button onclick="clearDisplay()">C</button>
            <button onclick="del()">DEL</button>
            <button onclick="percent()">%</button>
            <button onclick="add('/')">/</button>

            <br>

            <button onclick="add('7')">7</button>
            <button onclick="add('8')">8</button>
            <button onclick="add('9')">9</button>
            <button onclick="add('*')">*</button>

            <br>

            <button onclick="add('4')">4</button>
            <button onclick="add('5')">5</button>
            <button onclick="add('6')">6</button>
            <button onclick="add('-')">-</button>

            <br>

            <button onclick="add('1')">1</button>
            <button onclick="add('2')">2</button>
            <button onclick="add('3')">3</button>
            <button onclick="add('+')">+</button>

            <br>

            <button onclick="add('0')">0</button>
            <button onclick="add('.')">.</button>
            <button onclick="calculate()">=</button>

        </div>


        <script>

        let display = document.getElementById("display");


        function add(x){
            display.value += x;
        }


        function clearDisplay(){
            display.value="";
        }


        function del(){
            display.value =
            display.value.slice(0,-1);
        }


        function percent(){
            display.value =
            Number(display.value)/100;
        }


        function calculate(){

            try{
                display.value =
                eval(display.value);

            }
            catch{
                display.value="ERR";
            }

        }

        </script>

        """,
        height=430,
    )