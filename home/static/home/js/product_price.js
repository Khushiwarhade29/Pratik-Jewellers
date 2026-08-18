document.addEventListener("DOMContentLoaded", function(){

    const purity = document.querySelector("#id_purity");
    const weight = document.querySelector("#id_weight");

    const metalPrice = document.querySelector("#id_metal_price");
    const price = document.querySelector("#id_price");

    const making = document.querySelector("#id_making_charge");
    const stone = document.querySelector("#id_stone_charge");
    const gst = document.querySelector("#id_gst_percentage");


    function calculatePrice(){

        fetch(`/get-metal-rate/?purity=${purity.value}`)
        .then(response => response.json())
        .then(data => {


            let rate = parseFloat(data.rate);


            if(rate){

                // rate per 10 gram
                let perGram = rate / 10;


                let metal = perGram * parseFloat(weight.value || 0);


                metalPrice.value = metal.toFixed(2);



                // Making charge %

                let makingAmount =
                metal *
                parseFloat(making.value || 0)
                /100;



                // Hallmark

                let hallmark = 45;



                let subtotal =
                metal +
                makingAmount +
                parseFloat(stone.value || 0)
                +
                hallmark;



                // GST

                let gstAmount =
                subtotal *
                parseFloat(gst.value || 0)
                /100;



                let finalPrice =
                subtotal + gstAmount;



                price.value =
                finalPrice.toFixed(2);


            }

        });


    }



    purity.addEventListener("change", calculatePrice);
    weight.addEventListener("input", calculatePrice);
    making.addEventListener("input", calculatePrice);
    stone.addEventListener("input", calculatePrice);
    gst.addEventListener("input", calculatePrice);


});