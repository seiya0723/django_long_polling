window.addEventListener("load" , function (){

    //イベントをセットする要素が動的に変化する場合、documentからイベントを指定する
    $(document).on("click","#submit_form", function(){ submit_form(); });
    $(document).on("click",".trash", function(){ trash(this); });

    refresh();
});

function submit_form(){

    let form_elem   = "#form_area";

    let data    = new FormData( $(form_elem).get(0) );
    let url     = $(form_elem).prop("action");
    let method  = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (data.error){
            console.log("ERROR");
        }
        else{
            $("#content_area").html(data.content);
            $("#textarea").val("");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 
}

function trash(elem){

    let form_elem   = $(elem).parent("form");
    let url         = $(form_elem).prop("action");

    $.ajax({
        url: url,
        type: "DELETE",
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (data.error){
            console.log("ERROR");
        }
        else{
            $("#content_area").html(data.content);
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 
}


function refresh(){

    let value   = $("#first").val();
    let key     = $("#first").prop("name");

    query       = "?" + key + "=" + value;

    $.ajax({
        url: "refresh/" + query ,
        type: "GET",
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (data.error){
            console.log("ERROR");
        }
        else{
            $("#content_area").html(data.content);
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }).always( function(){

        //成功しても失敗しても実行されるalways
        console.log("refresh");

        //ロングポーリング(サーバー内で回すよう)に仕立てるので、リクエストの送信はほぼ即時で問題ない
        setTimeout(refresh, 500);

    });    
}
