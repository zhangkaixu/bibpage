function turn_note(i){
	x=document.getElementById("note_"+i).style.display
	if(x=='none')x='block'
	else x='none';
	document.getElementById("note_"+i).style.display=x
}