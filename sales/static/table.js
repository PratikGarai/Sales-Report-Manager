tables = document.getElementsByTagName("table");
for(let i=0; i<tables.length ; i++)
{
    tables[i].classList.add("table");
    tables[i].classList.add("table-hover");
    tables[i].classList.add("table-striped");
}