document.getElementById('extractButton').addEventListener('click', async () => {
    const sampleCase = document.getElementById('sampleCase').value;
    if (!sampleCase) {
        alert("Please enter a sample case.");
        return;
    }

    try {
        const response = await fetch('/extract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sampleCase })
        });
        
        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        const caseStatementsContainer = document.getElementById('caseStatementsContainer');
        caseStatementsContainer.innerHTML = "";

        if (data.extracted) {
            const entities = data.extracted.split('/').filter(word => word.trim() !== "");
            entities.forEach(entity => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.textContent = entity.trim();
                caseStatementsContainer.appendChild(tag);
            });
        } else {
            const noDataTag = document.createElement('div');
            noDataTag.className = 'tag';
            noDataTag.textContent = "No named entities found.";
            caseStatementsContainer.appendChild(noDataTag);
        }

        const roxieCaseStatementsTable = document.getElementById('roxieCaseStatementsTable');
        roxieCaseStatementsTable.innerHTML = '';

        if (data.caseStatements && data.caseStatements.length > 0) {
            const caseStatements = data.caseStatements.split(/\n/g).map(item => item.trim()).filter(item => item.length > 0);
            const displayLimit = 5;
            const limitedStatements = caseStatements.slice(0, displayLimit);

            limitedStatements.forEach((text, index) => {
                const rowElement = document.createElement('tr');

                const textCell = document.createElement('td');
                const truncatedText = text.length > 50 ? text.slice(0, 50) + "..." : text;
                textCell.textContent = truncatedText;

                const showMoreCell = document.createElement('td');
                const showMoreButton = document.createElement('button');
                showMoreButton.textContent = "Show more";
                
                showMoreButton.addEventListener('click', () => {
                    if (showMoreButton.textContent === "Show more") {
                        textCell.textContent = text;
                        showMoreButton.textContent = "Show less";
                    } else {
                        textCell.textContent = truncatedText;
                        showMoreButton.textContent = "Show more";
                    }
                });

                showMoreCell.appendChild(showMoreButton);
                rowElement.appendChild(textCell);
                rowElement.appendChild(showMoreCell);
                roxieCaseStatementsTable.appendChild(rowElement);
            });

            if (caseStatements.length > displayLimit) {
                const showMoreRow = document.createElement('tr');
                const showMoreCell = document.createElement('td');
                showMoreCell.colSpan = 2;
                const showMoreButton = document.createElement('button');
                showMoreButton.textContent = `Show ${caseStatements.length - displayLimit} more cases`;
                showMoreButton.addEventListener('click', () => {
                    caseStatements.slice(displayLimit).forEach((text) => {
                        const rowElement = document.createElement('tr');
                        const textCell = document.createElement('td');
                        const truncatedText = text.length > 50 ? text.slice(0, 50) + "..." : text;
                        textCell.textContent = truncatedText;
                        const showMoreCell = document.createElement('td');
                        const showMoreButton = document.createElement('button');
                        showMoreButton.textContent = "Show more";
                        showMoreButton.addEventListener('click', () => {
                            if (showMoreButton.textContent === "Show more") {
                                textCell.textContent = text;
                                showMoreButton.textContent = "Show less";
                            } else {
                                textCell.textContent = truncatedText;
                                showMoreButton.textContent = "Show more";
                            }
                        });
                        showMoreCell.appendChild(showMoreButton);
                        rowElement.appendChild(textCell);
                        rowElement.appendChild(showMoreCell);
                        roxieCaseStatementsTable.appendChild(rowElement);
                    });
                    showMoreRow.remove();
                });

                showMoreCell.appendChild(showMoreButton);
                showMoreRow.appendChild(showMoreCell);
                roxieCaseStatementsTable.appendChild(showMoreRow);
            }
        } else {
            const noDataRow = document.createElement('tr');
            const noDataCell = document.createElement('td');
            noDataCell.colSpan = 2;
            noDataCell.textContent = "No Roxie case statements found.";
            noDataRow.appendChild(noDataCell);
            roxieCaseStatementsTable.appendChild(noDataRow);
        }

    } catch (error) {
        console.error(error);
        document.getElementById('caseStatements').value = "Error connecting to server.";
    }
});



document.getElementById('submitPromptButton').addEventListener('click', async () => {
    const sampleCase = document.getElementById('sampleCase').value;
    const userPrompt = document.getElementById('userPrompt').value;

    if (!sampleCase || !userPrompt) {
        alert("Please enter both a sample case and a user prompt.");
        return;
    }

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sampleCase, userPrompt })
        });

        const data = await response.json();
        const backendResponse = document.getElementById('backendResponse');

        if (response.ok) {
            backendResponse.value = data.response || "No response.";
        } else {
            backendResponse.value = "Error: " + (data.error || "Failed to get response.");
        }

        backendResponse.style.height = "auto"; 
        backendResponse.style.height = backendResponse.scrollHeight + "px";

    } catch (error) {
        console.error(error);
    }
});