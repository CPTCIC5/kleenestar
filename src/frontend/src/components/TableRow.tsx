import { Check } from "lucide-react"
import avatar1 from '../../public/avatar1.png'
import avatar2 from "../../public/avatar2.png"
import avatar3 from "../../public/avatar3.png"
import avatar4 from "../../public/avatar4.png"
function TableRow({
	Invoice,
	Amount,
	Date,
	Status,
}: {
	Invoice: string
	Amount: number
	Date: string
	Status: string
}): JSX.Element {

	return (
		<tr className="last-of-type:border-t-0">
			<td className="flex text-left gap-4 text-[18px] font-bold items-center pl-[35.98px] py-[37.84px] border-t-[0.01px] border-solid border-t-gray-300">
				<input
					style={{ width: "50px", height: "20px" }}
					type="checkbox"
					name=""
					id=""
				/>
				{Invoice}
			</td>
			<td className="py-[30.84px] border-t-[0.01px] border-solid border-t-gray-300">
				USD {String(Amount)}
			</td>
			<td
				style={{ width: "25%" }}
				className="py-[30.84px] border-t-[0.01px] border-solid border-t-gray-300">
				{Date}
			</td>
			<td className="py-[30.84px] h-max-[84.5px] border-t-[0.01px] border-solid border-t-gray-300">
				{Status == "paid" ? (
					<span className="px-4 py-2 border-solid border border-royalblue text-royalblue rounded-3xl">
						<Check className="w-4 relative top-2 right-1" /> Paid
					</span>
				) : (
					<span className="px-4 py-2 border-solid border border-primary-300 rounded-3xl">
						Pending
					</span>
				)}
			</td>
			<td className="py-[30.84px] pl-36 border-t-[0.01px] border-solid border-t-gray-300">
				<div className="flex justify-evenly">
					<div className="border-solid relative right-10 bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
						<img
							src={avatar1}
							className="w-fit h-full"
							alt=""
						/>
					</div>
					<div className="border-solid relative right-[50px] bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
						<img
							src={avatar2}
							className="w-fit h-full"
							alt=""
						/>
					</div>
					<div className="border-solid relative right-[60px] bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
						<img
							src={avatar3}
							className="w-fit h-full"
							alt=""
						/>
					</div>
					<div className="border-solid relative right-[70px] bg-pink-300 border-2 w-10 h-10 border-primary-300 rounded-full object-cover object-center">
						<img
							src={avatar4}
							className="w-fit h-full"
							alt=""
						/>
					</div>
				</div>
			</td>
		</tr>
	)
}

export default TableRow
