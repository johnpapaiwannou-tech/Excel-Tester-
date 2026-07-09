import streamlit as st
import streamlit.components.v1 as components


def render_calculator():

    with st.sidebar:

        st.header("Αριθμομηχανή")

        components.html(
            """
            <style>

            body {
                overflow: hidden;
            }

            .calc {
                width: 250px;
                background: rgba(0,0,0,0.45);
                padding: 15px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }


            .display {
                width: 100%;
                height: 45px;
                font-size: 22px;
                text-align: right;
                border-radius: 12px;
                margin-bottom: 12px;
                border: none;
                padding: 5px 10px;
                background: rgba(255,255,255,0.15);
                color: white;
                box-sizing: border-box;
            }


            .row {
                display:flex;
                justify-content:center;
            }


            button {

                width:55px;
                height:45px;

                margin:3px;

                border-radius:12px;

                border:none;

                cursor:pointer;

                font-size:16px;

                background: rgba(255,255,255,0.15);

                color:white;

                transition:0.2s;

            }


            button:hover {

                background: rgba(255,255,255,0.35);

                transform: translateY(-2px);

            }


            .equal {

                background: rgba(0,120,255,0.65);

            }


            .clear {

                background: rgba(220,0,0,0.55);

            }


            </style>


            <div class="calc">

                <input id="display"
                       class="display"
                       value="0"
                       readonly>


                <div class="row">
                    <button class="clear" onclick="clearDisplay()">C</button>
                    <button onclick="deleteChar()">DEL</button>
                    <button onclick="percent()">%</button>
                    <button onclick="add('/')">/</button>
                </div>


                <div class="row">
                    <button onclick="add('7')">7</button>
                    <button onclick="add('8')">8</button>
                    <button onclick="add('9')">9</button>
                    <button onclick="add('*')">*</button>
                </div>


                <div class="row">
                    <button onclick="add('4')">4</button>
                    <button onclick="add('5')">5</button>
                    <button onclick="add('6')">6</button>
                    <button onclick="add('-')">-</button>
                </div>


                <div class="row">
                    <button onclick="add('1')">1</button>
                    <button onclick="add('2')">2</button>
                    <button onclick="add('3')">3</button>
                    <button onclick="add('+')">+</button>
                </div>


                <div class="row">
                    <button onclick="add('0')">0</button>
                    <button onclick="add('.')">.</button>
                    <button onclick="toggleSign()">+/-</button>
                    <button class="equal" onclick="calculate()">=</button>
                </div>


            </div>


            <script>


            let display = document.getElementById("display");


            function add(value){

                if(display.value === "0"){
                    display.value = value;
                }
                else{
                    display.value += value;
                }

            }


            function clearDisplay(){

                display.value="0";

            }



            function deleteChar(){

                if(display.value.length <=1){
                    display.value="0";
                }
                else{
                    display.value =
                    display.value.slice(0,-1);
                }

            }



            function percent(){

                try{

                    display.value =
                    Number(display.value)/100;

                }
                catch{

                    display.value="ERR";

                }

            }



            function toggleSign(){

                if(display.value.startsWith("-")){

                    display.value =
                    display.value.substring(1);

                }
                else{

                    display.value =
                    "-" + display.value;

                }

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
        