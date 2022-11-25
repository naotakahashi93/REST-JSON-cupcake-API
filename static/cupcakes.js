const BASE_URL = "http://127.0.0.1:5000/api";

console.log("HIII")
showCupcakeList();

function getCupcakeHTML(cupcake){ // function for creating each individual cupcake markup
return `<ul ${cupcake.id}>
    <li data.id=${cupcake.id}> ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
    <button class="delete-btn">X</button></br>
    <img class="cupcake-img"
            src="${cupcake.image}"
            width=200 
            height=auto>
    </li>
    <ul/>`

}

async function showCupcakeList(){ // function to list all the cupcakes
    const response = await axios.get(`${BASE_URL}/cupcakes`)//sending get request to cupcakes endpoint and waiting for reply
    for (let cupcake of response.data.cupcakes){
       let newcupcake = getCupcakeHTML(cupcake)
        $("#cupcakes-list").append(newcupcake)
    };
}

$("#submitnewcupcake").click(async function(){
    let flavor = $("#form-flavor").val()
    let size = $("#form-size").val()
    let rating = $("#form-rating").val()
    let image = $("#form-image").val()
    const response = await axios.post(`${BASE_URL}/cupcakes`, {flavor, size, rating, image})
    let newcupcake = getCupcakeHTML(response.data.cupcakes)
    $("#cupcakes-list").append(newcupcake)
    $("#newcupcakeform").trigger("reset")
})


$(document).on("click", ".delete-btn", async function(e){
    e.preventDefault();
    console.log(e.target);
    let $cupcake = $(e.target).closest("li");
    let id = $cupcake.attr("data.id");
    await axios.delete(`${BASE_URL}/cupcakes/${id}`);
    $cupcake.remove()
})


// async function deleteCupcake(){
//     e.preventDefault();
//     const id = $(this).data("id")
//     await axios.delete(`${BASE_URL}/cupcakes/${id}`)
// }