var loadValue = function(problemData) {
    var problem_type = e('.types').value
    var problem = e('.problem')
    if(problem_type == "SingleChoice" || problem_type == "MultipleChoice"){
        e('.topic').value = problemData.topic
        e('.option_A').value = problemData.option_A
        e('.option_B').value = problemData.option_B
        e('.option_C').value = problemData.option_C
        e('.option_D').value = problemData.option_D
        e('.answer').value = problemData.answer
        e('.analysis').value = problemData.analysis
    }
    else if(problem_type == "Judgement"){
        e('.topic').value = problemData.topic
        e('.answer').value = problemData.answer
        e('.analysis').value = problemData.analysis
    }
    else if(problem_type == "Analysis"){
        e('.topic').value = problemData.topic
        e('.answer').value = problemData.answer
    }
}

//var __main = function() {
//    loadInput()
//}

//__main()
