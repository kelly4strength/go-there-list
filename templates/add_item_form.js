"use strict";
// the above is setting the max number of item forms that I want to pop up
// the whole function is wrapped around this
$(document).ready(function() {
    console.log("setting fields")
    var max_fields = 7;
    var field = 1;

    // this funtion in calling the entire form class
    $("#itemForm")
        .on("submit", function(e){ 
            // .trim method trims out whitespace before and after string
            if ($(".form-control").val()) === "") {
                alert("Please fill out the entire form.");
                e.preventDefault();
            }
        })
        .on("click", ".addButton", function(e) {console.log("plus button clicked")
            if (field < max_fields) {
                $("#itemTemplate").clone()
                                 .removeAttr("hidden")
                                 .removeAttr("id")
                                 .insertBefore("#itemTemplate");
                field++;
            }
        })
        .on("click", ".removeButton", function(e) {
            if (field > 1){
                $(this).parents(".form-group").remove();  // Use the .parents() method to traverse up through the ancestors of the DOM tree
                field--;
            }
        });
        
});








