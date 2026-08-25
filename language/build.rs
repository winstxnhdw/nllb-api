fn main() -> Result<(), hf_hub::HFError> {
    let model_path = hf_hub::HFClientSync::new()?
        .model("facebook", "fasttext-language-identification")
        .download_file()
        .filename("model.bin")
        .send()?;

    println!("cargo:rerun-if-changed={}", model_path.display());
    println!("cargo:rerun-if-env-changed=HF_ENDPOINT");
    println!("cargo:rerun-if-env-changed=HF_HOME");
    println!("cargo:rerun-if-env-changed=HF_HUB_CACHE");
    println!(
        "cargo:rustc-env=FASTTEXT_MODEL_PATH={}",
        model_path.display()
    );

    Ok(())
}
