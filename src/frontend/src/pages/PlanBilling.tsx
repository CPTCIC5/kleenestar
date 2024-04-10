import { CircleArrowLeft, FolderClosed } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { plans } from "../utils/dummyPlans.json"
import { billing_details } from "../utils/dummyBilling.json"
import Plan from "../components/Plan"
import TableRow from "../components/TableRow"

function PlanBilling(): JSX.Element {
	const current_plan = "Scale"
	const navigate = useNavigate()
	return (
		<div className="w-screen h-full min-h-screen bg-background pb-80">
			<div className="w-full max-w-[1115] flex relative top-[73px] pl-8  ">
				<div className="text-primary-300 z-30 w-full  flex gap-8 items-center">
					<CircleArrowLeft
						className="w-[30px] h-[30px]  "
						onClick={() => navigate(-1)}
					/>
					<div className="text-primary-300 font-syne text-[1.6rem] font-bold">
						Plans and billing
					</div>
					<div className="font-syne rounded-xl px-[13px] py-[7px] font-[700] text-[17px] text-white bg-royalblue  ">
						Scale
					</div>
				</div>
				<div className="relative right-[110px] font-montserrat whitespace-nowrap text-[16px] font-[400] text-primary-300">
					<u>Manage plan and billing</u>
				</div>
			</div>
			<div className="px-[113px] w-max-[1512px]   mx-auto relative top-[148.14px]">
				<div className="flex gap-[36.01px] ">
					{plans.map((plan) => (
						<Plan
							{...plan}
							current_plan={current_plan}
						/>
					))}
				</div>
				<div className="w-full flex justify-between relative top-[43px] ">
					<p className="font-montserrat text-[18px] font-[600] text-primary-300 ">
						Billing details
					</p>
					<FolderClosed />
				</div>
				{/* Table */}
				<div className="bg-white w-full relative top-[60px] rounded-2xl">
					<table className="w-full text-[15px] font-montserrat font-[400] bg-white rounded-2xl">
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
					<div className="relative top-[62px] font-montserrat whitespace-nowrap text-[16px] font-[400] text-primary-300">
						<u>I need help with a bill issue</u>
					</div>
				</div>
			</div>
		</div>
	)
}

export default PlanBilling
