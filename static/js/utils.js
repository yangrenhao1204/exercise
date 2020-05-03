var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

var timeString = function(timestamp) {
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}


//ajax 函数
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json,非必须
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}


var SingleChoiceTemplate = function(){
    var p = `
        topic<input class="topic" type="text" name="topic"><br>
        <div class="options">
            A<input class="option_A" type="text" name="A"><br>
            B<input class="option_B" type="text" name="B"><br>
            C<input class="option_C" type="text" name="C"><br>
            D<input class="option_D" type="text" name="D"><br>
        </div>
        answer<input class="answer" type="text" name="answer"><br>
        analysis<input class="analysis" type="text" name="analysis">
    `
    return p
}


var MultipleChoiceTemplate = function(){
    var p = `
        topic<input class="topic" type="text" name="topic"><br>
        <div class="options">
            A<input class="option_A" type="text" name="A"><br>
            B<input class="option_B" type="text" name="B"><br>
            C<input class="option_C" type="text" name="C"><br>
            D<input class="option_D" type="text" name="D"><br>
        </div>
        answer<input class="answer" type="text" name="answer"><br>
        analysis<input class="analysis" type="text" name="analysis">
    `
    return p
}


var JudgementTemplate = function(){
    var p = `
        topic<input class="topic" type="text" name="topic"><br>
        answer<input class="answer" type="text" name="answer"><br>
        analysis<input class="analysis" type="text" name="analysis">
    `
    return p
}





var loadInput = function() {
    var problem_type = e('.types').value
    var problem_content = e('.problem_content')
    problem_content.innerHTML = ""
    if(problem_type == "SingleChoice"){
        problemCell = SingleChoiceTemplate()
    }
    else if(problem_type == "MultipleChoice"){
        problemCell = MultipleChoiceTemplate()
    }
    else if(problem_type == "Judgement"){
        problemCell = JudgementTemplate()
    }
    problem_content.insertAdjacentHTML('beforeend', problemCell)
}
