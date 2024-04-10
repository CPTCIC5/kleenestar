import { Check } from "lucide-react"

function Plan({price_m, plan_name, description, features, current_plan}: {price_m: number, plan_name: string
    , description: string, features: Array<string>, current_plan: string
}) : JSX.Element{
  return (
		<>
			{current_plan == plan_name ? (
				<div className="bg-primary-300 mq750:pr-[31px] text-white pb-[60px] flex-col max-w-[405.307px] w-full rounded-xl ">
					<p className=" relative left-[32.82px]  top-[23.28px] font-[700] text-[35px] pr-8  font-syne">
						${price_m}/month
					</p>
					<p className=" relative top-[20.58px] left-[32.82px] font-[600] font-montserrat text-[18px] ">
						{plan_name}
					</p>
					<p className=" leading-normal relative pr-[73.02px] top-[27.68px] left-[32.81px] font-[400] font-montserrat text-[15px]">
						{description}
					</p>
					<div className="bg-white h-[0.529px] mx-auto max-w-[90%] w-full relative top-[40.93px]"></div>

					<div className="relative top-[60.16px] left-[32.81px] pr-[20px]">
						{features.map((point) => {
							return (
								<>
									<div className="flex gap-2 items-center pb-[28.81px]">
										<div>
											<Check  className="bg-white w-[20x] p-1 h-fit rounded-full text-primary-300" />
										</div>
										<p className="pl-2 font-montserrat font-[500] text-[15px]">
											{point}
										</p>
									</div>
								</>
							)
						})}
					</div>
					<div className="text-royalblue relative top-[50.69px] mx-auto w-fit pb-[21.75px] font-montserrat font-[400] text-[15px] ">
						Current plan
					</div>
				</div>
			) : (
				<div className="mq750:hidden text-primary-300 bg-white h-full pb-[70px] flex-col max-w-[405.307px] w-full rounded-xl ">
					<p className=" relative left-[32.82px] top-[23.28px] pr-[20px] font-[700] text-[35px] font-syne">
						${price_m}/month
					</p>
					<p className=" relative top-[20.58px] left-[32.82px] font-[600] font-montserrat text-[18px] ">
						{plan_name}
					</p>
					<p className=" leading-normal relative pr-[73.02px] top-[27.68px] left-[32.81px] font-[400] font-montserrat text-[15px]">
						{description}
					</p>
					<div className="bg-primary-300 h-[0.529px] mx-auto max-w-[90%] w-full relative top-[40.93px]"></div>

					<div className="relative top-[60.16px] left-[32.81px] pr-[20px]">
						{features.map((point) => {
							return (
								<>
									<div className="flex gap-2 items-center pb-[28.81px]">
										<div>
											<Check className="bg-primary-300 w-[20x] p-1 h-fit rounded-full text-white" />
										</div>
										<p className="pl-2 font-montserrat font-[500] text-[15px]">
											{point}
										</p>
									</div>
								</>
							)
						})}
					</div>
					<div className=" relative top-[50.69px] mx-auto w-fit pb-[21.75px] font-montserrat font-[400] text-[15px] ">
						<u>Downgrade to Indie</u>
					</div>
				</div>
			)}
		</>
	)
}

export default Plan