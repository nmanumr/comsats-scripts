/**
 * Calculates invidual semester GPA rather than semester CGPA
 * 
 * Copy this script and paste in devtools console
 * when result card is opened on CUOnline
 */

let cpga = 0;
let n =0;
$(".single_result_container").each((i, el)=>{
    let weightSum = 0;
    let x = 0;

    $(el).find(".tbl_two [bordercolor]").each((i, d)=> {
        let e = $(d).find("td:last-of-type");
        if($(e).text().trim().length < 4 && parseFloat($(e).text().trim()) != NaN){
            weightSum += parseFloat($(e).text().trim()) * parseFloat($(d).find("td:nth-of-type(3)").text().trim());
            x += parseFloat($(d).find("td:nth-of-type(3)").text().trim());
        }
    });

    if (weightSum > 0) {
        console.log(`Semster ${n+1} GPA: ${(weightSum/x).toFixed(2)}`);
        cpga += (weightSum/x);
        n++;
    }
});

console.log("CGPA: " + (cpga/n).toFixed(2));