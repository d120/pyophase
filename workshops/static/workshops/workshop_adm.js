
(function($) {

    $(function() {
        /*
        $("div[data-assignment-id]").click(function() {
            var assId = $(this).attr("data-assignment-id");
            var slotId = $(this).attr("data-slot-id");
            var wsId = $(this).closest("[data-workshop-id]").attr("data-workshop-id");

            var orig = $(this).find("span").text();
            if (orig === "None") orig = "";
            var sc = assId === "None" ? "Add" : "Change";
            var entered = prompt(sc+" room assignment for \""+$(this).text()+"\" ?", orig);
            if (entered === null) return;
            if (entered === "") {
                if (assId !== "None") {
                    //DELETE
                }
            } else if (assId === "None") {
                // CREATE
                $.post("")
            } else if (assId !== "None") {
                // UPDATE

            }

        });*/
        setTimeout(()=>$("#id_assigned_location").select().focus(),1)
    })
})($ || jQuery || django.jQuery);

