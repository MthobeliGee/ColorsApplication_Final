
console.log("The List from away: ",list)

const app_pop = document.getElementById("app_pop")
const pop_header = document.getElementById("pop_header")
const pop_body = document.getElementById("pop_body")
function app_take(is_App_taking){
    app_pop.hidden = false
    pop_header.innerHTML = `
            <div>
                <b>Allow Applicants</b>
            </div>

            <div class="close2">
                <label onclick="togglePop()">Close</label>
            </div>

        `
    if(is_App_taking){
        pop_body.innerHTML=`
        
            <div>
                <p><b>Are you sure you want to "Close" this colors application to take 'Applicants'</b></p>
            </div>
            <hr/>
            <div class="action_btn">
                <div>
                    <button id="btn_yes" onclick="isAllowClose(true)" class="btn btn-default btn-success">Yes</button>
                </div>
                <div>

                    <button id="btn_yes" onclick="isAllowClose(false)" class="btn btn-default btn-danger">No</button>
                </div>

            </div>

        
        `
    }
    else{
        
        pop_body.innerHTML=`
        
            <div>
                <p><b>Are you sure you want to allow this colors application to take 'Applicants'</b></p>
            </div>
            <hr/>
            <div class="action_btn">
                <div>
                    <button id="btn_yes" onclick="isAllow(true)" class="btn btn-default btn-success">Yes</button>
                </div>
                <div>

                    <button id="btn_yes" onclick="isAllow(false)" class="btn btn-default btn-danger">No</button>
                </div>

            </div>

        
        `


    }
}

function isAllow(is_app_allow){
    console.log("is_app_allow: ", is_app_allow)
    domain = document.getElementById("domain").value
    if(is_app_allow){

        document.getElementById("action").value = "Allowed";

        document.getElementById("sub_App_take").click();
        

    }
    else{
        togglePop()
    }
}

function isAllowClose(is_app_allow){
    console.log("is_app_allow: ", is_app_allow)
   
    if(is_app_allow){

        document.getElementById("action").value = "DisAllowed";

        document.getElementById("sub_App_take").click();
        

    }
    else{
        togglePop()
    }
}


function togglePop(){
    app_pop.hidden = true
}