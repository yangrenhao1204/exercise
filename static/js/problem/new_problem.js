var get_chapter_list = function(subject_id, callback) {
    var path = '/problem/get_chapter_list?subject_id=' + subject_id
    ajax('GET', path, '', callback)
}


var insert_chapter = function(chapter){
    var chapter_select = e(".chapters")
    var cell = `
         <option value="${chapter.id}">${chapter.name}</option>
    `
    chapter_select.insertAdjacentHTML('beforeend', cell)
}


var change_suject = function(){
    var sub = e(".sujects");
    var subject_id = sub.options[sub.selectedIndex].value;
    e(".chapters").innerHTML = ""
    get_chapter_list(subject_id, function(r){
        chapter_list = JSON.parse(r)
        for(var i = 0; i < chapter_list.length; i++) {
            var chapter = chapter_list[i]
            insert_chapter(chapter)
        }
    })
}


var change_type = function(){
    loadInput()
}

