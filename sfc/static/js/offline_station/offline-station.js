function check_cpuSN() {
    var cpu_sn = document.forms["p_part_input_form"]["Cpu_SN"].value;
    if (cpu_sn == "") {
        return false;
    }
    return true;
}

function check_hSN() {
    var h_sn = document.forms["p_part_input_form"]["H_SN"].value;
    if (h_sn == "") {
        return false;
    }
    return true;
}

function submitForm() {
    if (check_cpuSN() && check_hSN()) {
        return true;
    }
    alert("Missing Field");
    return false;
}