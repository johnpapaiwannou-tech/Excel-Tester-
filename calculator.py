import streamlit as st
import streamlit.components.v1 as components


def render_calculator():

    with st.sidebar:

        st.header("Αριθμομηχανή")

        components.html(
            """

            <style>

            body {
                margin:0;
                padding:0;
                overflow:hidden;
            }


            .calc {

                width:230px;

                background:rgba(0,0,0,0.45);

                padding:14px;

                border-radius:20px;

                backdrop-filter:blur(12px);

                box-shadow:
                0 15px 40px rgba(0,0,0,0.35);

            }


            .display {

                width:100%;

                height:45px;

                box-sizing:border-box;

                background:
                rgba(255,255,255,0.12);

                color:white;

                border:none;

                border-radius:12px;

                padding:8px 12px;

                font-size:22px;

                text-align:right;

                margin-bottom:12px;

                outline:none;

            }



            .row {

                display:flex;

                justify-content:space-between;

                margin-bottom:6px;

            }



            button {

                width:48px;

                height:42px;

                border:none;

                border-radius:12px;

                background:
                rgba(255,255,255,0.15);

                color:white;

                font-size:16px;

                cursor:pointer;

                transition:0.2s;

            }



            button:hover {

                background:
                rgba(255,255,255,0.35);

                transform:translateY(-2px);

            }



            .operator {

                background:
                rgba(0,120,255,0.45);

            }



            .equal {

                background:
                rgba(0,180,90,0.55);

            }



            .clear {

                background:
                rgba(220,50,50,0.55);

            }


            </style>




            <div class="calc">


            <input 
            id="display"
            class="display"
            value="0"
            readonly>



            <div class="row">

                <button class="clear"
                onclick="clearDisplay()">
                C
                </button>

                <button onclick="del()">
                DEL
                </button>

                <button onclick="percent()">
                %
                </button>

                <button class="operator"
                onclick="add('/')">
                /
                </button>

            </div>




            <div class="row">

                <button onclick="add('7')">
                7
                </button>

                <button onclick="add('8')">
                8
                </button>

                <button onclick="add('9')">
                9
                </button>

                <button class="operator"
                onclick="add('*')">
                *
                </button>

            </div>





            <div class="row">

                <button onclick="add('4')">
                4
                </button>

                <button onclick="add('5')">
                5
                </button>

                <button onclick="add('6')">
                6
                </button>

                <button class="operator"
                onclick="add('-')">
                -
                </button>

            </div>





            <div class="row">

                <button onclick="add('1')">
                1
                </button>

                <button onclick="add('2')">
                2
                </button>

                <button onclick="add('3')">
                3
                </button>

                <button class="operator"
                onclick="add('+')">
                +
                </button>

            </div>





            <div class="row">

                <button onclick="add('0')">
                0
                </button>

                <button onclick="add('.')">
                .
                </button>

                <button onclick="toggleSign()">
                +/-
                </button>

                <button class="equal"
                onclick="calculate()">
                =
                </button>

            </div>



            </div>





            <script>


            let display =
            document.getElementById("display");



            function add(x){

                if(display.value=="0")
                {
                    display.value=x;
                }

                else
                {
                    display.value+=x;
                }

            }



            function clearDisplay(){

                display.value="0";

            }




            function del(){

                let value =
                display.value.slice(0,-1);


                if(value=="")
                {
                    value="0";
                }


                display.value=value;

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

                if(display.value.startsWith("-"))
                {

                    display.value =
                    display.value.substring(1);

                }

                else
                {

                    display.value =
                    "-"+display.value;

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
            height=370,
        )