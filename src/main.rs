extern crate clap;
extern crate ansi_term;
extern crate reqwest;
extern crate serde_json;

#[macro_use]
extern crate serde_derive;

use clap::{App, Arg, crate_name, crate_version, crate_authors, crate_description};
use ansi_term::Colour;
use serde_json::{Deserializer, Value};

pub static API_URL: &'static str = "https://cve.circl.lu/api";xw

fn main() {
    let conflicts_all_vendors = ["vendor-name", "cve-id", "config"];
    let conflicts_vendor_name = ["all-vendors", "cve-id", "config"];
    let conflicts_cve_id = ["all-vendors", "vendor-name", "config"];
    let conflicts_config = ["all-vendors", "vendor-name", "cve-id"];

    let matches = App::new(crate_name!())
        .version(crate_version!())
        .about(crate_description!())
        .author(crate_authors!())
        .arg(Arg::with_name("all-vendors")
            .long("all-vendors")
            .short("a")
            .takes_value(false)
            .conflicts_with_all(&conflicts_all_vendors)
            .help("Show all vendors"))
        .arg(Arg::with_name("vendor-name")
            .long("products")
            .short("p")
            .takes_value(true)
            .conflicts_with_all(&conflicts_vendor_name)
            .help("Show all products for vendor"))
        .arg(Arg::with_name("cve-id")
            .long("cve")
            .short("i")
            .takes_value(true)
            .conflicts_with_all(&conflicts_cve_id)
            .help("Show info for CVE (example: --cve CVE-2010-3333)"))
        .arg(Arg::with_name("config")
            .long("config")
            .short("c")
            .takes_value(true)
            .conflicts_with_all(&conflicts_config)
            .help("Config path (example: --vendors.toml"))
        .get_matches();

    if matches.is_present("all-vendors") {
        show_all_vendors()
            .ok();
    } else if let Some(vendor_name) = matches.value_of("vendor-name") {
        show_products_by_vendor(vendor_name.to_string());
    } else if let Some(cve_id) = matches.value_of("cve-id") {
        show_cve_info(cve_id.to_string());
    } else if let Some(config) = matches.value_of("config") {
        parse_config(config.to_string());
    } else {
        println!("{}", Colour::Red.bold().paint("Something went wrong, use --help flag"));
    }
}

fn show_all_vendors() -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", Colour::Green.bold().paint("All available vendors:"));

    let url_all_vendors = format!("{}/browse", API_URL);
    let output_all_vendors = reqwest::blocking::get(&url_all_vendors)?
        .text()?;
    Ok(())
}

fn show_products_by_vendor(vendor_name: String) {
    println!("Product is: {}", vendor_name);
}

fn show_cve_info(cve_id: String) {
    println!("CVE is: {}", cve_id);
}

fn parse_config(config: String) {
    println!("Config path is: {}", config);
}
