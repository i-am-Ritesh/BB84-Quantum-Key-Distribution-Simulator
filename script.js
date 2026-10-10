// Flask backend URL
const API_URL = "http://127.0.0.1:5000/simulate";
const simulateButton = document.getElementById("simulateButton");
const numBits = document.getElementById("numBits");
const noise = document.getElementById("noise");
const eve = document.getElementById("eve");
const noiseValue = document.getElementById("noiseValue");
const keyLength = document.getElementById("keyLength");
const qber = document.getElementById("qber");
const eveStatus = document.getElementById("eveStatus");
const noiseDisplay = document.getElementById("noiseDisplay");
const aliceBits = document.getElementById("aliceBits");
const aliceBases = document.getElementById("aliceBases");
const bobBases = document.getElementById("bobBases");
const bobBits = document.getElementById("bobBits");
const eveBases = document.getElementById("eveBases");
const eveBits = document.getElementById("eveBits");
const siftAlice = document.getElementById("siftAlice");
const siftBob = document.getElementById("siftBob");
const secretKey = document.getElementById("secretKey");
const log = document.getElementById("log");
noise.addEventListener("input", function () {
    noiseValue.innerHTML = Number(noise.value).toFixed(2);
});
function arrayToString(value) {
    if (value == null)
        return "-";
    if (Array.isArray(value))
        return value.join(" ");
    return value.toString();
}
function writeLog(message) {
    log.value += "\n" + message;
    log.scrollTop = log.scrollHeight;
}
function clearOutput() {
    aliceBits.innerHTML = "";
    aliceBases.innerHTML = "";
    bobBases.innerHTML = "";
    bobBits.innerHTML = "";
    eveBases.innerHTML = "";
    eveBits.innerHTML = "";
    siftAlice.innerHTML = "";
    siftBob.innerHTML = "";
    secretKey.innerHTML = "";
    keyLength.innerHTML = "-";
    qber.innerHTML = "-";
}
function populate(sim) {
    aliceBits.innerHTML = arrayToString(sim.alice_bits);
    aliceBases.innerHTML = arrayToString(sim.alice_bases);
    bobBases.innerHTML = arrayToString(sim.bob_bases);
    bobBits.innerHTML = arrayToString(sim.bob_results);
    siftAlice.innerHTML = arrayToString(sim.sifted_alice);
    siftBob.innerHTML = arrayToString(sim.sifted_bob);
    secretKey.innerHTML = arrayToString(sim.secret_key);
    keyLength.innerHTML = sim.secret_key_length;
    qber.innerHTML = sim.qber;
    eveStatus.innerHTML = sim.eve_enabled ? "Enabled" : "Disabled";
    noiseDisplay.innerHTML = sim.noise_probability;
    if (sim.eve_enabled) {
        eveBases.innerHTML = arrayToString(sim.eve_bases);
        eveBits.innerHTML = arrayToString(sim.eve_results);
    }
    else {
        eveBases.innerHTML = "-";
        eveBits.innerHTML = "-";
    }
}
async function runSimulation() {
    clearOutput();
    log.value = "";
    writeLog("Starting BB84 Simulation...");
    const payload = {
        num_bits: parseInt(numBits.value),
        eve: eve.checked,
        noise_probability: parseFloat(noise.value)
    };
    writeLog("Sending request to Flask server...");
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`HTTP ${response.status}: ${text}`);
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || "Simulation failed.");
    }
        populate(data.simulation);
        writeLog("Simulation Completed Successfully.");
        writeLog("Secret Key Length : " + data.simulation.secret_key_length);
        writeLog("QBER : " + data.simulation.qber);
        writeLog("Simulation Finished.");
    }
    catch (error) {
        console.error("Simulation Error:", error);
        alert(error.message);
        writeLog(error.message);
    }
}
simulateButton.addEventListener(
    "click",
    runSimulation
);
noiseValue.innerHTML = Number(noise.value).toFixed(2);
log.value =
`BB84 Quantum Key Distribution Simulator
Ready.
Configure the parameters and press
"Run Simulation".`;