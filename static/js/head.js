var _hmt = _hmt || [];
        (function() {
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?cdef6708f1dc40904a5927911ec338c8";
            var s = document.getElementsByTagName("script")[0]; 
            s.parentNode.insertBefore(hm, s);
        })();

var usertext=""
var initext="hi,你是Q宝，一款真正懂你的啥b智能语音助手"
var aitext="1"
//计时器变量
var fishAlert;
//弹出功能函数
function textShow_ai(num){
    $("#bubble_ai").removeClass("end")
    $("#bubble_ai").removeClass("toastAni")
    if(aitext==""||(num&&num==1))
        return;
    $("#bubble_ai").html(aitext).addClass("toastAni")
    
    console.log("textshow")
    fishAlert=setTimeout(function(){
        $("#bubble_ai").addClass("end")
        $("#bubble_ai").removeClass("toastAni")
        console.log("end")
    },1000)

}

function textinit(){
    $("#bubble").removeClass("end")
    $("#bubble").removeClass("toastAni")
    $("#bubble").html(initext).addClass("toastAni")
    
    console.log("textshow")
    fishAlert=setTimeout(function(){
        $("#bubble").addClass("end")
        $("#bubble").removeClass("toastAni")
        console.log("end")
    },1000)

}

$(document).ready(function(){
    //动画时间4000ms，间隔时间8000ms
        textinit()
})


function textShow(){
    $("#bubble_r").removeClass("end")
    $("#bubble_r").removeClass("toastAni")
    if(usertext=="")
        return 1;
    $("#bubble_r").html(usertext).addClass("toastAni")
    
    console.log("textshow")
    fishAlert=setTimeout(function(){
        $("#bubble_r").addClass("end")
        $("#bubble_r").removeClass("toastAni")
        console.log("end")
    },1000)

}

var re_json;

function stext()
{
    usertext=$("#utext").val()
        textShow_ai(textShow())
    // re_json={{login_ornot|tojson}}
    initsvg()
}




