import { CircleArrowLeft, CreditCardIcon, FolderClosed } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { plans } from "../utils/dummyPlans.json"
import { billing_details } from "../utils/dummyBilling.json"
import Plan from "../components/Plan"
import TableRow from "../components/TableRow"
import avatar1 from "../../public/avatar1.png"
import avatar2 from "../../public/avatar2.png"
import avatar3 from "../../public/avatar3.png"
import avatar4 from "../../public/avatar4.png"

function PlanBilling(): JSX.Element {
	const current_plan = "Scale"
	const navigate = useNavigate()
	return (
		<div className="w-screen h-full min-h-screen bg-background pb-80 mq750:pb-20">
			<div className="w-full max-w-[1115] mx-auto flex relative mq750:top-[0px] top-[73px] pl-8 mq750:pl-0  ">
				<div className="text-primary-300 mq750:justify-between mq750:px-[32px] mq750:py-[30px] mq750:bg-white z-30 w-full text-center	  flex gap-8 items-center">
					<CircleArrowLeft
						className="w-[30px] mq750:w-[23px] h-[30px]   "
						onClick={() => navigate(-1)}
					/>
					<div className="text-primary-300 mq750:text-[20px] whitespace-nowrap font-syne text-[1.6rem] font-bold">
						Plans and billing
					</div>
					<div className="font-syne mq750:absolute mq750:top-[118.5px] mq750:left-[36.75px] rounded-xl px-[13px] py-[7px] font-[700] text-[17px] text-white bg-royalblue  ">
						Scale
					</div>
					<div className="mq750:flex hidden  mq750:absolute mq750:top-[118.5px] mq750:left-[50%]">
						<div className="border-solid relative  bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
							<img
								src={avatar1}
								className="w-fit h-full"
								alt=""
							/>
						</div>
						<div className="border-solid relative right-[10px] bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
							<img
								src={avatar2}
								className="w-fit h-full"
								alt=""
							/>
						</div>
						<div className="border-solid relative right-[20px] bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
							<img
								src={avatar3}
								className="w-fit h-full"
								alt=""
							/>
						</div>
						<div className="border-solid relative right-[30px] bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
							<img
								src={avatar4}
								className="w-fit h-full"
								alt=""
							/>
						</div>
					</div>
					<CreditCardIcon className="hidden mq750:block " />
				</div>
				<div className="mq750:hidden relative right-[110px] font-montserrat whitespace-nowrap text-[16px] font-[400] text-primary-300">
					<u>Manage plan and billing</u>
				</div>
			</div>
			<div className="px-[113px] mq750:px-[31px] w-max-[1512px] mx-auto relative top-[148.14px]">
				<div className="flex gap-[36.01px] ">
					{plans.map((plan) => (
						<Plan
							{...plan}
							current_plan={current_plan}
						/>
					))}
				</div>
				<div className="mq750:hidden w-full flex justify-between relative top-[43px] ">
					<p className="font-montserrat text-[18px] font-[600] text-primary-300 ">
						Billing details
					</p>
					<FolderClosed />
				</div>
				{/* Table */}
				<div className=" bg-white w-full relative top-[60px] rounded-2xl">
					<table className="w-full mq750:hidden text-[15px] font-montserrat font-[400] bg-white rounded-2xl">
						<thead className="text-center">
							<tr className="">
								<td className="py-[30.84px] flex items-center pl-[35.98px] ">
									<input
										style={{ width: "50px", height: "20px" }}
										type="checkbox"
										name=""
										id=""
									/>
									Invoice
								</td>
								<td
									className="py-[30.84px] "
									style={{ width: "25%" }}>
									Amount
								</td>
								<td
									className="py-[30.84px] "
									style={{ width: "25%" }}>
									Date
								</td>
								<td className="py-[30.84px]">Status</td>
								<td
									className="py-[30.84px]"
									style={{ width: "25%" }}>
									Users
								</td>
							</tr>
						</thead>
						<tbody className="text-center">
							{billing_details.map((bill) => (
								<TableRow {...bill} />
							))}
						</tbody>
					</table>
					<div className="relative top-[62px] mq750:top-[-30px]  mq650:text-center font-montserrat whitespace-nowrap text-[16px] font-[400] text-primary-300">
						<u>I need help with a bill issue</u>
					</div>
				</div>
			</div>
		</div>
	)
}

export default PlanBilling
