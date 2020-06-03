extern crate clap;

use clap::{App, Arg, crate_name, crate_version, crate_authors, crate_description};
use std::ffi::OsString;

#[cfg(test)]
extern crate quickcheck;
#[cfg(test)]
#[macro_use(quickcheck)]
extern crate quickcheck_macros;

#[derive(Debug, PartialEq)]
struct HelloArgs {
    name: String,
}

impl HelloArgs {
    fn new() -> Self {
        Self::new_from(std::env::args_os().into_iter()).unwrap_or_else(|e| e.exit())
    }

    fn new_from<I, T>(args: I) -> Result<Self, clap::Error>
    where
        I: Iterator<Item = T>,
        T: Into<OsString> + Clone,
    {
        // Basic app information
        let app = App::new(crate_name!())
            .version(crate_version!())
            .about(crate_description!())
            .author(crate_authors!());

        // CLI options
        let vendors_option = Arg::with_name("vendors")
            .long("vendors")
            .short("v")
            .takes_value(true)
            .help("Show all vendors")
            .required(false);

        // Define the name command line option
        /*let name_option = Arg::with_name("name")
            .long("name") // allow --name
            .short("n") // allow -n
            .takes_value(true)
            .help("Who to say hello to")
            .required(true);*/

        // now add in the argument we want to parse
        let app = app.arg(vendors_option);
        // extract the matches
        let matches = app.get_matches_from_safe(args)?;

        // Extract the actual name
        let name = matches
            .value_of("vendors")
            .expect("This can't be None, we said it was required");

        Ok(HelloArgs {
            name: name.to_string(),
        })
    }
}

fn main() {
    let hello = HelloArgs::new();

    println!("Hello, {}!", hello.name);
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_no_args() {
        HelloArgs::new_from(["exename"].iter()).unwrap_err();
    }

    #[test]
    fn test_incomplete_name() {
        HelloArgs::new_from(["exename", "--name"].iter()).unwrap_err();
    }

    #[test]
    fn test_complete_name() {
        assert_eq!(
            HelloArgs::new_from(["exename", "--name", "Hello"].iter()).unwrap(),
            HelloArgs { name: "Hello".to_string() }
        );
    }

    #[test]
    fn test_short_name() {
        assert_eq!(
            HelloArgs::new_from(["exename", "-n", "Hello"].iter()).unwrap(),
            HelloArgs { name: "Hello".to_string() }
        );
    }

    #[quickcheck]
    fn prop_never_panics(args: Vec<String>) {
        let _ignored = HelloArgs::new_from(args.iter());
    }
}

/*
+ 1. Show all vendors in table: [0-9], [A-P], etc: curl http://cve.circl.lu/api/browse
+ 2. Show all products for the vendor: [0-9], [A-P], etc: curl http://cve.circl.lu/api/browse/microsoft
- (limited api) 3. Show all cves for product: curl http://cve.circl.lu/api/search/microsoft/office
+ 4. Show CVE info: curl http://cve.circl.lu/api/cve/CVE-2010-3333
-5. get latest updates: curl http://cve.circl.lu/api/last
6. Show all CVES for products in list for the selected date
*/
