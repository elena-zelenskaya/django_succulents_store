$(function () {
	function changeImage() {
		var imageSrc = $(this).attr("src");
		$(this).attr("src", $(this).attr("hover-src"));
		$(this).attr("hover-src", imageSrc);
	}
	$(".succulents").hover(changeImage, changeImage);
	$("#cookie_modal").modal("show");
	$("#dialog")
		.dialog({
			resizable: false,
			dialogClass: "no-close",
			modal: true,
			minWidth: "300",
			autoOpen: false,
			position: { my: "center top", at: "center top", of: window },
			buttons: [
				{
					text: "Ok",
					click: function () {
						$(this).dialog("close");
					},
				},
			],
			create: function (e, ui) {
				$(".no-close button:last").addClass(
					"ui-button ui-corner-all ui-widget"
				);
			},
		})
		.html(`<p>Your Cart is empty!</p>`);
	$("#shopping_cart").click(function (e) {
		e.preventDefault();
		$("#dialog").dialog("open");
	});

	// $.get(
	// 	"https://fakestoreapi.herokuapp.com/products/",
	// 	function (data) {
	// 		console.log(data);
	// 		for (var i = 0; i < data.length; i++) {
	// 			var correctLink =
	// 				"https://fakestoreapi.herokuapp.com/" +
	// 				data[i].image.substring(25);
	// 			$("main .row").append(`
	// 			<div class="col-lg-2 col-md-4 col-sm-6 col-xs-6">
	// 				<a href="">
	// 					<img src="${correctLink}" alt="${data[i].title}" />
	// 					<p>${data[i].title}</p>
	// 					<p>$${data[i].price}</p>
	// 				</a>
	// 			</div>`);
	// 		}
	// 	},
	// 	"json"
	// );

	// fetch("https://fakestoreapi.herokuapp.com/products", { mode: "no-cors" })
	// 	.then((res) => res.json())
	// 	.then((json) => console.log(json));
});
