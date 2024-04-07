import { Circle, CircleArrowLeft } from "lucide-react"
import { useNavigate } from "react-router-dom"
import json from '../utils/dummyConnectChannels.json'
import ChannelCard from "../components/ChannelCard"

function ConnectChannels() {
  const channel: {
		name: string
		image: string
		description: string
		connected: boolean
		available: boolean
	}[] = json.data.channels

  const navigate = useNavigate()
  return (
		<div className="w-full bg-background ">
			<div className="w-full mq750:justify-between mq750:px-[32px] text-primary-300 items-center relative top-[69px] gap-[30px] flex pl-[50px]">
				<CircleArrowLeft
					className="w-[30px] h-[30px]  "
					onClick={() => navigate(-1)}
				/>
				<span className="font-syne font-[700] mq750:text-[20px] text-[30px] leading-[36px]">
					My channels
				</span>
				<span className="mq750:block hidden text-primary-300">
					<div className=" w-fit h-fit rounded-full font-bold px-[8px] flex items-center border-solid py-[1px] border-[1.5px] border-primary-300 text-primary-300">
						?
					</div>
				</span>
			</div>
			<div className="w-full max-w-[1478px] font-montserrat font-[400] text-[16px]">
				<div className="w-full mq750:text-center flex mq750:px-[31.5px] px-[110px] justify-between relative top-[123.74px]">
					<span className="w-full">
						Connect the marketing channels you use.
					</span>
					<div className="mq750:hidden py-[1px] w-fit h-fit rounded-full font-bold px-[8px] flex items-center border-solid border-2 border-primary-300 text-primary-300">
						?
					</div>
				</div>
			</div>
			<div className="w-full bg-background pb-10 flex-wrap gap-[35.8px] flex font-montserrat relative top-[175.83px]   max-w-[1478px] justify-center">
				{channel.map((props) => {
					return <ChannelCard {...props} />
				})}
			</div>
		</div>
	)
}

export default ConnectChannels