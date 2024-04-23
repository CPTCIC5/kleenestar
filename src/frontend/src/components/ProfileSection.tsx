import { PencilLine } from "lucide-react"
import { ChangeEvent, useEffect, useRef, useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import parsePhoneNumber, { CountryCode } from "libphonenumber-js"
import { getNames, registerLocale } from "i18n-iso-countries"
import english from "i18n-iso-countries/langs/en.json"
import CustomSelect from "./CustomSelect"
import Cookies from "js-cookie"
import axios, { AxiosError } from "axios"
import {toast} from 'sonner'

registerLocale(english)

const countryList = Object.entries(getNames("en")).map(([value, name]) => ({
	value: value,
	label: name,
}))
type FormFields = z.infer<typeof schema>

const schema = z.object({
	first_name: z
		.string()
		.min(5, "The first name should be at least 5 characters long")
		.max(100, "The first name should not exceed 100 characters")
		.regex(/^[a-zA-Z '-]+$/, "Name can only include letters and hypen(-)")
		,
	last_name: z
		.string()
		.min(5, "The last name should be at least 5 characters long")
		.max(100, "The last name should not exceed 100 characters")
		.regex(/^[a-zA-Z '-]+$/, "Name can only include letters and hypen(-)"),
	email: z.string().email({ message: "Invalid email address" }),
	workspace: z
		.string()
		.min(5, "Workspace name should have atleast 5 characters")
		.max(100, "Workspace length should not exceed 100 characters ")
		.regex(
			/^[a-zA-Z0-9 _-]+$/,
			"Workspace name can include letters, underscores, hypens(-) and numbers only"
		)
		,
	country: z.string().min(1, { message: "Country is required" }),
	number: z
		.string()
		.min(10, {
			message: "Invalid Phone Number",
		}),
})

function ProfileSection(): JSX.Element {
	const [avatar, setAvatar] = useState("")
	const [userDetails, setUserDetails] = useState<{ id: string , profile: {country: string} }>({
		id: "",
		profile: {
			country: ""
		}
	})
	const [isValid, setIsValid] = useState(false)
	const imageRef = useRef<HTMLInputElement>(null)
	const handleAvatarClick = () => {
		if (imageRef.current) {
			imageRef.current.click()
		}
	}
	const handleAvatarUpload = async(e: ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if(!file){
			return
		}else{
			const formData = new FormData()
			formData.append("profile[avatar]", file)
			console.log(formData)
			const user_id = userDetails.id
			try{
				await axios.patch(
					`http://127.0.0.1:8000/api/auth/users/${user_id}/`,
					formData,
					{
						withCredentials: true,
						headers: {
							"Content-Type": "multipart/form-data",
							"X-CSRFToken": Cookies.get("csrftoken"),
						},
					}
				)
			}catch(err){
				console.error(err)
			}
		}	

	}
	const form = useForm<FormFields>({
		defaultValues: {
			first_name: "",
			last_name: "",
			email: "",
			workspace: "",
			country: "india",
			number: "",
		},
		resolver: zodResolver(schema),
		mode: "onChange",
	})

	const { register, formState, setError, control, reset, clearErrors, watch } =
		form
	const { errors, isDirty, dirtyFields } = formState
	
	useEffect(() => {
		Object.keys(errors).forEach((fieldName) => {
			if (!dirtyFields[fieldName as keyof typeof dirtyFields] && fieldName !== 'country') {
				clearErrors(fieldName as keyof typeof dirtyFields) // Add type assertion
			}
			if(fieldName === "country"){
				if(watch().country){
					clearErrors("country")
				}
			}
		})
		if (Object.keys(errors).length > 0) {
			setIsValid(false)
		} else {
			setIsValid(true)
		}
	}, [dirtyFields, errors, clearErrors, Object.keys(errors)])

	useEffect(() => {
		const fetchWorkspaceDetails = async () => {
			const response = await axios.get(
				"http://127.0.0.1:8000/api/workspaces/",
				{
					withCredentials: true,
					headers: {
						"Content-Type": "application/json",
						"X-CSRFToken": Cookies.get("csrftoken"),
					},
				}
			)
			const formDetails = response.data[0]
			setUserDetails(response.data[0].root_user)

			reset({
				first_name: formDetails.root_user.first_name || "",
				last_name: formDetails.root_user.last_name || "",
				email: formDetails.root_user.email || "",
				workspace: formDetails.business_name || "",
				country: formDetails.root_user.profile.country || "",
				number: formDetails.root_user.profile.phone_number || "",
			})
			setAvatar(formDetails.root_user.profile.avatar)
		}
		fetchWorkspaceDetails()
	}, [reset])
	
	const getConfig = (data: { [key: string]: string }) => {
		const config: { [key: string]: any } = {}
		const profile: { [key: string]: string } = {}

		Object.keys(data).forEach((key) => {
			if (dirtyFields[key as keyof typeof dirtyFields]) {
				if (data[key]) {
					if (key === "number") {
						profile["phone_number"] = data[key]
					} else if (key === "country") {
						profile["country"] = data[key]
					} else {
						config[key] = data[key]
					}
				}
			}
		})

		if (profile["phone_number"] || profile["country"]) {
			config["profile"] = profile
			// profile["user"] = userDetails.id
		}

		return config
	}
	
	const onSubmit = async() => {
		const data = watch()
		if (data.number) {
			if (!data.country) {
				setError("country", {
					message: "Country Not Selected!",
				})
				setIsValid(false)
				return
			} else {
				
				const validPhoneNumber = parsePhoneNumber(data.number, {
					defaultCountry: data.country as CountryCode,
					extract: false,
				})
			if (
				!validPhoneNumber ||
				!validPhoneNumber.isValid() ||
				!(validPhoneNumber.country === data.country)
			) {
				setError("number", {
					message: "Invalid Phone Number",
				})
				setIsValid(false)
				return
			}
			}
		}
		const config = getConfig(data)
		console.log(config)
		const user_id = userDetails.id
		console.log(user_id)
		if(config){
			try {
				await axios.patch(
					`http://127.0.0.1:8000/api/auth/users/${user_id}/`,
					config,
					{
						withCredentials: true,
						headers: {
							"X-CSRFToken": Cookies.get("csrftoken"),
							"Content-Type": "application/json",
						},
					}
				)
				toast.success("Profile Saved Successfully")
			} catch (err) {
				if (
					(err as AxiosError).response &&
					(err as AxiosError)?.response?.status === 400 &&
					(err as AxiosError)?.response?.data?.user[0]
				) {
					toast.success("Profile Saved Successfully")
				} else {
					console.error(err)
					toast.error("Failed to save profile")
				}
				
			}
		}
	}

	return (
		<div className="w-[50%] bg-white mq1000:w-[95%] mq1000:mx-auto rounded-[2rem] ">
			<div className="text-primary-300  font-montserrat pt-[28px] pl-8 pb-4 mq1000:pl-4 border-solid border-b-2 border-[#BEB9B1] ">
				<p className=" font-bold text-[16px]"> Profile</p>
				<p className="text-[14px] pt-2  whitespace-nowrap">
					Mange your profile details
				</p>
			</div>
			<div className="py-4 flex items-center gap-4 pl-8 ">
				<div className="w-fit bg-gradient-to-b from-amber-100 to-peach-200 h-fit rounded-full py-[3.5rem] px-[3.6rem] mq1000:px-[2.2rem] mq1000:py-[2.2rem] border-solid border-primary-300 border-4 "></div>
				<div>
					<input
						ref={imageRef}
						className="hidden"
						type="file"
						name="files"
						id=""
						onChange={handleAvatarUpload}
					/>
					<img
						onClick={handleAvatarClick}
						src={"/add_image.png"}
						className="w-[30px] mq1000:w-6"
						alt=""
					/>
				</div>
			</div>
			<div className="p-2 pt-4  w-full font-montserrat text-lg ">
				<div className="w-[95%] mx-auto">
					<div className="flex  justify-center mq1000:flex-col gap-4">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							First name
							<div className="w-full mt-2 bg-background rounded-[2rem] p-4 flex items-center h-[45px] ">
								<input
									{...register("first_name")}
									type="text"
									placeholder="First name"
									className="font-montserrat autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.first_name && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.first_name.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Last name
							<div className="w-full mt-2 bg-background h-[45px] rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("last_name")}
									type="text"
									placeholder="Last name"
									className="autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full font-montserrat  text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.last_name && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.last_name.message}
								</div>
							)}
						</div>
					</div>
					<div className="flex  justify-center gap-4 pt-2 mq1000:flex-col">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Email address
							<div className="w-full h-[45px] mt-2 bg-[#D1D3DB] rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("email")}
									type="text"
									placeholder="Email address"
									className="autofill:bg-transparent outline-none bg-transparent font-montserrat w-full text-[15px] bg-clip-text"
								/>
								<PencilLine className="text-primary-300 bg-transparent" />
							</div>
							{errors.email && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.email.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Workspace name
							<div className="w-full mt-2 h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("workspace")}
									type="text"
									placeholder="Workspace name"
									className="autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.workspace && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.workspace.message}
								</div>
							)}
						</div>
					</div>
					<div className="flex  justify-center gap-4 pt-2 mq1000:flex-col">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Country
							<div className="relative w-full h-[45px] flex items-center mt-2">
								<CustomSelect
									name="country"
									control={control}
									placeholder={userDetails.profile.country || "Country"}
									options={countryList}
								/>
							</div>
							{errors.country && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.country.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Phone number
							<div className="w-full h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("number")}
									type="text"
									placeholder="Phone number"
									className="autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.number && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.number.message}
								</div>
							)}
						</div>
					</div>
					{isDirty && isValid ? (
						<div
							onClick={onSubmit}
							className="w-full font-bold rounded-[2rem] my-8 cursor-pointer text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
							Save changes
						</div>
					) : (
						<div onClick={()=>{toast.warning("Please make some changes to save!")}}  className="w-full font-bold rounded-[2rem] cursor-default  bg-opacity-50  my-8  text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
							Save changes
						</div>
					)}
				</div>
			</div>
		</div>
	)
}

export default ProfileSection
