document.addEventListener("DOMContentLoaded", function () {

    const purity = document.getElementById("id_purity");
    const weight = document.getElementById("id_weight");
    const price = document.getElementById("id_price");

    if (!purity || !weight || !price) return;

    async function calculatePrice() {

        if (purity.value === "" || weight.value === "") {
            return;
        }

        try {
            const response = await fetch(`/get-metal-rate/?purity=${purity.value}`);
            const data = await response.json();

            if (data.rate) {

                const metalRate = parseFloat(data.rate);
                const wt = parseFloat(weight.value);

                price.value = (metalRate * wt).toFixed(2);

            }

        } catch (e) {
            console.log(e);
        }

    }

    purity.addEventListener("change", calculatePrice);
    weight.addEventListener("input", calculatePrice);

});