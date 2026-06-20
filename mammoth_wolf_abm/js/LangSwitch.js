// set default language here
let lang = "en"

navbar = document.getElementById("navbar")
config = { attributes: true, childList: true, subtree: true }

navbar.innerHTML += `
<div><p>Tab</p></div>
<div id="lang-flag">
<img width="64" src="rabbitgrassweed/pics/Flag_of_Hungary.svg" alt="Set language to Hungarian">
</div>
`

// Initialize description
fetch("rabbitgrassweed/docs/eng_description.md")
    .then(response => response.text())
    .then(text => description.innerHTML = text)

startButton = document.getElementById("play-pause")
stepButton = document.getElementById("step")
resetButton = document.getElementById("reset")
currentStep = document.getElementById("currentStep").parentElement

currentStep.outerHTML = `<span id="currentStepText">Current Step: </span><span id="currentStep">0</span>`
currentStep = document.getElementById("currentStepText")

fpsText = document.getElementById("elements-topbar").firstElementChild.firstElementChild

StartButtonCallback = (mutationList) => {
    if (lang === "hu") {
        for (const mutation of mutationList) {
            if (startButton.firstElementChild.innerText === "Start") {
                startButton.firstElementChild.innerText = "Indítás"
            }
            else if (startButton.firstElementChild.innerText === "Stop") {
                startButton.firstElementChild.innerText = "Megállítás"
            }
        }
    }
};

const StartButtonObserver = new MutationObserver(StartButtonCallback);
StartButtonObserver.observe(startButton.firstElementChild, config);

const description = document.getElementsByClassName("modal-body")[0].firstElementChild

function SwitchToHun() {
    HeaderToHun()
    ButtonsToHun()
    ParamsToHun()
    lang_flag.firstElementChild.src = "rabbitgrassweed/pics/Flag_of_the_United_Kingdom_(1-2).svg"
    lang_flag.firstElementChild.alt = "Nyelv angolra állítása"
    lang = "hu"
}

function HeaderToHun() {
    document.title = "Nyulak, fű és gyomnövények (Mesa vizualizáció)"
    document.getElementsByClassName("navbar-brand")[0].innerText = "Nyulak, fű és gyomnövények"
    document.getElementsByClassName("modal-title")[0].innerText = "Nyulak, fű és gyomnövények leírás"

    fetch("rabbitgrassweed/docs/hun_description.md")
        .then(response => response.text())
        .then(text => description.innerHTML = text)
}

function ButtonsToHun() {
    if (!controller.running)
        startButton.firstElementChild.innerText = "Indítás"
    else
        startButton.firstElementChild.innerText = "Megállítás"

    stepButton.firstElementChild.innerText = "Léptetés"
    resetButton.firstElementChild.innerText = "Visszaállítás"
    currentStep.innerText = "Jelenlegi lépés: "
    navbar.firstElementChild.firstElementChild.firstElementChild.innerText = "Leírás"
    fpsText.innerText = "Képkocka per másodperc"
}

function ParamsToHun() {
    // Torus
    let torus = document.getElementById("torus_id")
    torus.parentElement.firstElementChild.innerText = "Tórusz"
    // Model type
    let model_type = document.getElementById("model_type_id")
    model_type.parentElement.firstElementChild.firstElementChild.innerText = "Modelltípus"
    model_type.children[0].innerText = "Bővített modell"
    model_type.children[1].innerText = "Nyulak, fű és gyomnövények modell"
    model_type.children[2].innerText = "Rókák és nyulak Lotka-Volterra-modell"
    // Initial number of rabbits
    document.getElementById("n_rabbit_id_tooltip").innerText = "A nyulak kezdeti száma"
    // Initial number of foxes
    document.getElementById("n_fox_id_tooltip").innerText = "A rókák kezdeti száma"
    // EP gain from eating grass (rabbits)
    document.getElementById("rabbit_ep_gain_grass_id_tooltip").innerText =
        "Fűből nyert EP (nyulak)"
    // EP gain from eating weeds (rabbits)
    document.getElementById("rabbit_ep_gain_weed_id_tooltip").innerText =
        "Gyomnövényekből nyert EP (nyulak)"
    // EP gain from eating rabbits (foxes)
    document.getElementById("fox_ep_gain_id_tooltip").innerText =
        "Nyulakból nyert EP (rókák)"
    // Rabbits' maximal initial EP
    document.getElementById("rabbit_max_init_ep_id_tooltip").innerText =
        "A nyulak maximális kezdeti EP-je"
    // Foxes' maximal initial EP
    document.getElementById("fox_max_init_ep_id_tooltip").innerText =
        "A rókák maximális kezdeti EP-je"
    // Rabbits' reproduction threshold (EP)
    document.getElementById("rabbit_reproduction_threshold_id_tooltip").innerText =
        "A nyulak szaporodási küszöbe (EP)"
    // Foxes' reproduction threshold (EP)
    document.getElementById("fox_reproduction_threshold_id_tooltip").innerText =
        "A rókák szaporodási küszöbe (EP)"
    // Grass' regrow rate (%)
    document.getElementById("grass_regrow_rate_id_tooltip").innerText = "A fű visszanövési rátája (%)"
    // Weeds' regrow rate (%)
    document.getElementById("weed_regrow_rate_id_tooltip").innerText = "A gyomnövények visszanövési rátája (%)"
    // Allow flocking
    let allow_flocking = document.getElementById("allow_flocking_id")
    allow_flocking.parentElement.firstElementChild.innerText = "Csordába szerveződés engedélyezése"
    // Allow hunt
    let allow_hunt = document.getElementById("allow_hunt_id")
    allow_hunt.parentElement.firstElementChild.innerText = "Vadászat engedélyezése"
    // Hunt limiter exponent
    let hunt_exponent = document.getElementById("hunt_exponent_id")
    hunt_exponent.parentElement.firstElementChild.firstElementChild.innerText = "A vadászatot korlátozó kitevő"
    // Allow Seed
    let allow_seed = document.getElementById("allow_seed_id")
    allow_seed.parentElement.firstElementChild.innerText = "Seed engedélyezése"
    // Random Seed
    let seed = document.getElementById("random_seed_id")
    seed.parentElement.firstElementChild.firstElementChild.innerText = "Random seed"
}

function SwitchToEng() {
    HeaderToEng()
    ButtonsToEng()
    ParamsToEng()
    lang_flag.firstElementChild.src = "rabbitgrassweed/pics/Flag_of_Hungary.svg"
    lang_flag.firstElementChild.alt = "Set language to Hungarian"
    lang = "en"
}

function HeaderToEng() {
    document.title = "Rabbits, Grass and Weeds (Mesa visualization)"
    document.getElementsByClassName("navbar-brand")[0].innerText = "Rabbits, Grass and Weeds"
    document.getElementsByClassName("modal-title")[0].innerText = "About Rabbits, Grass and Weeds"

    fetch("rabbitgrassweed/docs/eng_description.md")
        .then(response => response.text())
        .then(text => description.innerHTML = text)
}

function ButtonsToEng() {
    if (!controller.running)
        startButton.firstElementChild.innerText = "Start"
    else
        startButton.firstElementChild.innerText = "Stop"
    navbar.firstElementChild.firstElementChild.firstElementChild.innerText = "About"
    stepButton.firstElementChild.innerText = "Step"
    resetButton.firstElementChild.innerText = "Reset"
    currentStep.innerText = "Current Step: "
    fpsText.innerText = "Frames Per Second"
}

function ParamsToEng() {
    // Torus
    let torus = document.getElementById("torus_id")
    torus.parentElement.firstElementChild.innerText = "Torus"
    // Model type
    let model_type = document.getElementById("model_type_id")
    model_type.parentElement.firstElementChild.firstElementChild.innerText = "Model type"
    model_type.children[0].innerText = "Extended model"
    model_type.children[1].innerText = "Rabbits, Grass and Weeds model"
    model_type.children[2].innerText = "Foxes and Rabbits Lotka-Volterra model"
    // Initial number of rabbits
    document.getElementById("n_rabbit_id_tooltip").innerText = "Initial number of rabbits"
    // Initial number of foxes
    document.getElementById("n_fox_id_tooltip").innerText = "Initial number of foxes"
    // EP gain from eating grass (rabbits)
    document.getElementById("rabbit_ep_gain_grass_id_tooltip").innerText =
        "EP gain from eating grass (rabbits)"
    // EP gain from eating weeds (rabbits)
    document.getElementById("rabbit_ep_gain_weed_id_tooltip").innerText =
        "EP gain from eating weeds (rabbits)"
    // EP gain from eating rabbits (foxes)
    document.getElementById("fox_ep_gain_id_tooltip").innerText =
        "EP gain from eating rabbits (foxes)"
    // Rabbits' maximal initial EP
    document.getElementById("rabbit_max_init_ep_id_tooltip").innerText =
        "Rabbits' maximal initial EP"
    // Foxes' maximal initial EP
    document.getElementById("fox_max_init_ep_id_tooltip").innerText =
        "Foxes' maximal initial EP"
    // Rabbits' reproduction threshold (EP)
    document.getElementById("rabbit_reproduction_threshold_id_tooltip").innerText =
        "Rabbits' reproduction threshold (EP)"
    // Foxes' reproduction threshold (EP)
    document.getElementById("fox_reproduction_threshold_id_tooltip").innerText =
        "Foxes' reproduction threshold (EP)"
    // Grass' regrow rate (%)
    document.getElementById("grass_regrow_rate_id_tooltip").innerText = "Grass' regrow rate (%)"
    // Weeds' regrow rate (%)
    document.getElementById("weed_regrow_rate_id_tooltip").innerText = "Weeds' regrow rate (%)"
    // Allow flocking
    let allow_flocking = document.getElementById("allow_flocking_id")
    allow_flocking.parentElement.firstElementChild.innerText = "Allow flocking"
    // Allow hunt
    let allow_hunt = document.getElementById("allow_hunt_id")
    allow_hunt.parentElement.firstElementChild.innerText = "Allow hunt"
    // Hunt limiter exponent
    let hunt_exponent = document.getElementById("hunt_exponent_id")
    hunt_exponent.parentElement.firstElementChild.firstElementChild.innerText = "Hunt limiter exponent"
    // Allow Seed
    let allow_seed = document.getElementById("allow_seed_id")
    allow_seed.parentElement.firstElementChild.innerText = "Allow Seed"
    // Random Seed
    let seed = document.getElementById("random_seed_id")
    seed.parentElement.firstElementChild.firstElementChild.innerText = "Random Seed"
}

const lang_flag = document.getElementById("lang-flag")
if (lang_flag !== null)
{
    lang_flag.onclick = () => {
        if (lang === "en") {
            SwitchToHun()
        }
        else if (lang === "hu") {
            SwitchToEng()
        }
    }
}
