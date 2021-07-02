/**
 * Auto submits the feedback on CuOnline. why? firstly no body cares about our feedback 2ndly why its compulsory?
 * 
 * How to run this script
 * 
 * - Step 1: Install ths chrome extension:
 *      https://chrome.google.com/webstore/detail/custom-javascript-for-web/ddbjnfjiigjmcpcpkmhogomapikjbjdk
 * - Step 2: Login to your CUOnline account.
 * - Step 3: Click on the extension icon and paste this script.
 * - Step 4: Hit save button and take some rest.
 */

let stars = () => 1 + Math.round(Math.random() * 4);
// uncomment this if you want fixed stars
// stars = () => 3;

// 'SUBJECT_CODE': [COURSE_STARS, FACULTY_STARS]
// for example `'CSE356': [1, 1]`
const specialSubjects = {
}

if (window.location.pathname == '/Feedback') {
    (function() {
        $(".quiz_listing tr").each((i, el) => {
            if(
                $(el).attr("onclick")
                && $(el).attr("onclick").toString().match(/window/)
                && !$(el).text().match(/UnAvailable/i)
            ){
                $(el).click();
                return;
            }
        });
    })();
}
else if (window.location.pathname.match(/Survey/)) {
    $(`.rating`).each((i, e) => {
        for (let ss in specialSubjects) {
            let title = $(".content_area>div:first-of-type").text();
            let isFaculty = title.match("Faculty");

            if (title.toLowerCase().match(ss.toLowerCase())) {
                let s
                if (Array.isArray(specialSubjects[ss]) && specialSubjects[ss].length > 1) {
                    s = specialSubjects[ss][isFaculty ? 1 : 0];
                } else if (typeof specialSubjects[ss] === 'number') {
                    s = specialSubjects[ss];
                } else {
                    s = stars();
                }

                $(e).find(`[value=${6 - s}]`).click();
                return;
            }
        }

        $(e).find(`[value=${6 - stars()}]`).click();
    })
    $("#txtcomments").val('WowCoolPostThanksForSharing<3');
    $('#SubmitBtn').click();
}
