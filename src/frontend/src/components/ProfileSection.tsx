import { PencilLine } from "lucide-react"
import { ChevronDown } from "lucide-react"
import {useRef} from 'react'
import SelectOptions from "./SelectOptions";


function ProfileSection(): JSX.Element {
	const countries = [
		"Afghanistan",
		"Albania",
		"Algeria",
		"Andorra",
		"Angola",
		"Antigua and Barbuda",
		"Argentina",
		"Armenia",
		"Australia",
		"Austria",
		"Azerbaijan",
		"Bahamas",
		"Bahrain",
		"Bangladesh",
		"Barbados",
		"Belarus",
		"Belgium",
		"Belize",
		"Benin",
		"Bhutan",
		"Bolivia",
		"Bosnia and Herzegovina",
		"Botswana",
		"Brazil",
		"Brunei",
		"Bulgaria",
		"Burkina Faso",
		"Burundi",
		"Cabo Verde",
		"Cambodia",
		"Cameroon",
		"Canada",
		"Central African Republic",
		"Chad",
		"Chile",
		"China",
		"Colombia",
		"Comoros",
		"Congo, Democratic Republic of the",
		"Congo, Republic of the",
		"Costa Rica",
		"Croatia",
		"Cuba",
		"Cyprus",
		"Czech Republic",
		"Denmark",
		"Djibouti",
		"Dominica",
		"Dominican Republic",
		"East Timor (Timor-Leste)",
		"Ecuador",
		"Egypt",
		"El Salvador",
		"Equatorial Guinea",
		"Eritrea",
		"Estonia",
		"Eswatini",
		"Ethiopia",
		"Fiji",
		"Finland",
		"France",
		"Gabon",
		"Gambia",
		"Georgia",
		"Germany",
		"Ghana",
		"Greece",
		"Grenada",
		"Guatemala",
		"Guinea",
		"Guinea-Bissau",
		"Guyana",
		"Haiti",
		"Honduras",
		"Hungary",
		"Iceland",
		"India",
		"Indonesia",
		"Iran",
		"Iraq",
		"Ireland",
		"Israel",
		"Italy",
		"Ivory Coast",
		"Jamaica",
		"Japan",
		"Jordan",
		"Kazakhstan",
		"Kenya",
		"Kiribati",
		"Korea, North",
		"Korea, South",
		"Kosovo",
		"Kuwait",
		"Kyrgyzstan",
		"Laos",
		"Latvia",
		"Lebanon",
		"Lesotho",
		"Liberia",
		"Libya",
		"Liechtenstein",
		"Lithuania",
		"Luxembourg",
		"Madagascar",
		"Malawi",
		"Malaysia",
		"Maldives",
		"Mali",
		"Malta",
		"Marshall Islands",
		"Mauritania",
		"Mauritius",
		"Mexico",
		"Micronesia",
		"Moldova",
		"Monaco",
		"Mongolia",
		"Montenegro",
		"Morocco",
		"Mozambique",
		"Myanmar (Burma)",
		"Namibia",
		"Nauru",
		"Nepal",
		"Netherlands",
		"New Zealand",
		"Nicaragua",
		"Niger",
		"Nigeria",
		"North Macedonia",
		"Norway",
		"Oman",
		"Pakistan",
		"Palau",
		"Palestine",
		"Panama",
		"Papua New Guinea",
		"Paraguay",
		"Peru",
		"Philippines",
		"Poland",
		"Portugal",
		"Qatar",
		"Romania",
		"Russia",
		"Rwanda",
		"Saint Kitts and Nevis",
		"Saint Lucia",
		"Saint Vincent and the Grenadines",
		"Samoa",
		"San Marino",
		"Sao Tome and Principe",
		"Saudi Arabia",
		"Senegal",
		"Serbia",
		"Seychelles",
		"Sierra Leone",
		"Singapore",
		"Slovakia",
		"Slovenia",
		"Solomon Islands",
		"Somalia",
		"South Africa",
		"South Sudan",
		"Spain",
		"Sri Lanka",
		"Sudan",
		"Suriname",
		"Sweden",
		"Switzerland",
		"Syria",
		"Taiwan",
		"Tajikistan",
		"Tanzania",
		"Thailand",
		"Togo",
		"Tonga",
		"Trinidad and Tobago",
		"Tunisia",
		"Turkey",
		"Turkmenistan",
		"Tuvalu",
		"Uganda",
		"Ukraine",
		"United Arab Emirates",
		"United Kingdom",
		"United States",
		"Uruguay",
		"Uzbekistan",
		"Vanuatu",
		"Vatican City",
		"Venezuela",
		"Vietnam",
		"Yemen",
		"Zambia",
		"Zimbabwe",
	]
	const imageRef = useRef<HTMLInputElement>(null);
	const handleAvatarClick = () => {
		if (imageRef.current) {
			imageRef.current.click();
		}
	};
	return (
		<div className="w-[50%] bg-white mq750:w-[95%] mq750:mx-auto rounded-[2rem] ">
			<div className="text-primary-300 font-montserrat pt-2 pl-8 pb-4 mq750:pl-4 border-solid border-b-2 border-[#BEB9B1] ">
				<p className=" font-bold text-[1.6rem] mq750:text-[16px]"> Profile</p>
				<p className="mq750:text-[14px] whitespace-nowrap">
					Mange your profile details
				</p>
			</div>
			<div className="py-4 flex items-center gap-4 pl-8 ">
				<div className="w-fit bg-gradient-to-b from-amber-100 to-peach-200 h-fit rounded-full py-[3.5rem] px-[3.6rem] mq750:px-[2.2rem] mq750:py-[2.2rem] border-solid border-primary-300 border-4 "></div>
				<div>
					<input
						ref={imageRef}
						className="hidden"
						type="file"
						name="files"
						id=""
					/>
					<img
						onClick={handleAvatarClick}
						src="/add_image.png"
						className="w-[30px] mq750:w-6"
						alt=""
					/>
				</div>
			</div>
			<div className="p-2 pt-4  w-full font-montserrat text-lg ">
				<div className="w-[95%] mx-auto">
					<div className="flex items-center justify-center mq750:flex-col gap-4">
						<div className="w-full text-primary-300 font-bold text-xl mq750:text-[14px]">
							Frist name
							<div className="w-full mt-2 bg-background rounded-[2rem] p-4 flex items-center mq750:h-[45px] ">
								<input
									type="text"
									placeholder="First name"
									className="font-montserrat w-full text-xl mq750:text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
						<div className="w-full text-primary-300 font-bold text-xl mq750:text-[14px]">
							Last name
							<div className="w-full mt-2 bg-background mq750:h-[45px] rounded-[2rem] p-4 flex items-center ">
								<input
									type="text"
									placeholder="Last name"
									className="w-full font-montserrat  text-xl mq750:text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="flex items-center justify-center gap-4 pt-2 mq750:flex-col">
						<div className="w-full text-primary-300 font-bold text-xl mq750:text-[14px]">
							Email address
							<div className="w-full mq750:h-[45px] mt-2 bg-[#D1D3DB] rounded-[2rem] p-4 flex items-center ">
								<input
									pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
									type="text"
									placeholder="Email address"
									className="font-montserrat w-full text-xl mq750:text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
						<div className="w-full text-primary-300 font-bold text-xl mq750:text-[14px]">
							Workspace name
							<div className="w-full mt-2 mq750:h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									type="text"
									placeholder="Workspace name"
									className="w-full font-montserrat text-xl mq750:text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="flex items-center justify-center gap-4 pt-2 mq750:flex-col">
						<div className="w-full text-primary-300 font-bold text-xl mq750:text-[14px]">
							Country
							<div className="w-full px-[19.34px]  mt-2 bg-background  rounded-[2rem]  flex items-center ">
								<SelectOptions
									options={countries}
									InputText={"Country"}
								/>
								<ChevronDown className="text-primary-300" />
							</div>
						</div>
						<div className="w-full text-primary-300 font-bold text-xl mq750:text-[14px]">
							Phone number
							<div className="w-full mq750:h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									type="text"
									placeholder="Phone number"
									className="w-full font-montserrat text-xl mq750:text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="w-full font-bold rounded-[2rem] my-8 cursor-pointer text-white mq750:text-[15px] mq750:py-[0.7rem] bg-primary-300 text-center py-[1rem]">
						Save changes
					</div>
				</div>
			</div>
		</div>
	)
}

export default ProfileSection
