"use strict";

var searchID = 0;

function updateDisplayedMaxAge(age) {
    
    
    document.getElementById("max_age_notif").textContent = "You will see the offers published less than " + age + " days ago (use the slider below to change that setting)";
    
}
function toggleLoadingScreen() {

    
    if (document.getElementById("loading").style.display === "") {
        
        document.getElementById("loading").style.display = "block";
    } else {
        
        document.getElementById("loading").style.display = "";
    }
    
}

function downloadCSV() {
    

    document.getElementById("hidden_form").submit();
    
    return True;
}

function newSearch() {
    
    
    document.getElementById("results_page").remove();
    document.getElementById("main_zone").style.display = "flex";
    document.getElementById("use_instructions").style.display = "block";
    
    
    
    return True;
    
}

function displayResults(JSONresults)    {
    
    let results = JSON.parse(JSONresults);
    

    
    toggleLoadingScreen();
    document.getElementById("main_zone").style.display = "none";
    document.getElementById("use_instructions").style.display = "none";
    
    
    let resultsPage = document.createElement('div');
    resultsPage.id = "results_page";
    
    let resultsCount = results.length;
    
    if (resultsCount === 0) {
        
        let noResultsMessage = document.createElement("span");
        noResultsMessage.innerHTML = "We could not find any job offer matching your search";
        noResultsMessage.id = "no_results_message";
        let newSearchBtn = document.createElement("button");
        newSearchBtn.innerHTML = "New Search";
        newSearchBtn.onclick = newSearch;
        newSearchBtn.className = "results_header_btn";
        
        
        
        
        resultsPage.append(noResultsMessage);
        resultsPage.append(newSearchBtn);
        //document.body.append(resultsPage);
        document.getElementById("main_zone").after(resultsPage);
        
        return True;
    }
    
    let resultsPageHeader = document.createElement('div');
    resultsPageHeader.id = "results_page_header";
    
    let headerCaption = document.createElement("span");
    headerCaption.id = "header_caption";
    
    
    
    if (resultsCount === 1) {
        
        headerCaption.innerHTML = "1 offer found";
    }
    
    else {
        
        headerCaption.innerHTML = resultsCount.toString() + " offers found";
    }
    
    let disclaimer = document.createElement("span");
    disclaimer.id = "disclaimer";
    disclaimer.innerHTML = "(Some results might have been omitted due to technical issues on the job boards JobsMiner parses)"
    
    
    let headerButtons = document.createElement("div");
    headerButtons.id = "header_buttons";
    let newSearchBtn = document.createElement("button");
    newSearchBtn.innerHTML = "New Search";
    newSearchBtn.onclick = newSearch;
    newSearchBtn.className = "results_header_btn";
    let csvBtn = document.createElement("button");
    csvBtn.innerHTML = "Download CSV file";
    
    csvBtn.className = "results_header_btn";
    
    let csvHiddenForm = document.createElement("form");
    csvHiddenForm.id = "hidden_form";
    csvHiddenForm.style.display = "none";
    csvHiddenForm.action = "/download";
    csvHiddenForm.method = "POST";
    
    let csvHiddenInputField = document.createElement("input");
    csvHiddenInputField.type = "hidden";
    csvHiddenInputField.name = "uniqueID";
    csvHiddenInputField.value = searchID;
    
    csvBtn.onclick = downloadCSV;
    
    
    headerButtons.append(newSearchBtn);
    headerButtons.append(csvBtn);
    headerButtons.append(csvHiddenForm);
    csvHiddenForm.append(csvHiddenInputField);
    
    resultsPageHeader.append(headerCaption);
    resultsPageHeader.append(disclaimer);
    resultsPageHeader.append(headerButtons);
    
    let resultsTable = document.createElement('table');
    resultsTable.id = "results_table";
    
    resultsTable.insertAdjacentHTML("afterbegin", "<tr><th id='job_title_col'>Job title</th><th id='website_col'>Website</th><th id='age_col'>Age</th></tr>");
    
    
    for (let i=0; i<results.length; i++) {
        
        if(Array.isArray(results[i][0])) {
            
            for(let j=0; j<results[i].length; j++) {

                if (results[i][j][3] == "0") {
                    
                    var age = "<24 hours ago";
                }
                else if (results[i][j][3] == "1") {
                    
                    var age = "1 day";
                }
                else if (results[i][j][3] == "30") {
                    
                    var age = "30+ days";
                }
                else {
                    
                    var age = results[i][j][3] + " days";
                }
                

                let newLine =  "<tr><td><a href='" + results[i][j][1] + "'>" + results[i][j][0] + "</a></td><td>" +
                    results[i][j][2] + "</td><td>" +
                    age + "</td></tr>";
                
                resultsTable.insertAdjacentHTML("beforeend", newLine);
            }
        } else {
            
            
            
            if (results[i][3] == "0") {
                    
                var age = "<24 hours ago";
            }
            else if (results[i][3] == "1") {
                    
                var age = "1 day";
            }
            else if (results[i][3] == "30") {
                    
                var age = "30+ days";
            }
            else {
                    
                var age = results[i][3] + " days";
            }
   
            
            let newLine =  "<tr><td><a href='" + results[i][1] + "'>" + results[i][0] + "</a></td><td>" +
                    results[i][2] + "</td><td>" +
                    age + "</td></tr>";
                
                resultsTable.insertAdjacentHTML("beforeend", newLine);
        }
        
    }
    
    
    resultsPage.append(resultsPageHeader);
    resultsPage.append(resultsTable);
    //document.body.append(resultsPage);
    document.getElementById("main_zone").after(resultsPage);

    
}

function displayServerError(jqXHR, textStatus, errorThrown)    {
    
    alert(jqXHR + "\n" + textStatus + "\n" + errorThrown);
}

function validateFormFields() {
    
    if ($('#jobTitle').val() == "" || $('#location').val() == "" || $('#country').val() == "") {
        
        return false;
    }
    
    return true;
}

function search() {
    
    if (!validateFormFields()) {
        
        return false
    }
    
    toggleLoadingScreen();
    
    let jobTitle = $('#jobTitle').val();
    let location = $('#location').val();
    let country = $('#country').val();
    let age = $('#age').val();
    
    searchID = Math.round(Date.now());
    
    $.post("/search", {jobTitle: jobTitle,
                      location: location,
                      country: country,
                      age: age,
                      uniqueID : searchID}).done(function(response){
        
        displayResults(response);
        
    }).fail(function(jqXHR, textStatus, errorThrown){
        
        displayServerError(jqXHR, textStatus, errorThrown)
    });
    
    return false;
    
}




    
   