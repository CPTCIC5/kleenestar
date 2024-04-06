import * as React from 'react'
import SlideSwitch from './SlideSwitch';
import { RefreshCcw } from 'lucide-react';

interface ChannelCards {
    name: string;
    image: string;
    description: string;
    connected: boolean;
    available: boolean;
}


function ChannelCard ({
    name, image, description, connected, available
}: ChannelCards) {
  return (
		<>
			{available ? (
				<div className="mq750:mx-[31.63px] max-w-[407.48px]  bg-white px-[23.5px] w-full max-h-[291.95px] mq750:max-h-[300.95px]  rounded-[2rem]">
					<img
						className="w-[51px] h-[51px] mt-[10px]"
						src={image}
						alt=""
					/>
					<div className="w-full  font-[600] text-primary-300 text-[18px] ">
						{name}
					</div>
					<div className="w-full pt-[10px] mq750:pb-[15px] pb-[17px]  text-[15px]  font-[400px] leading-[28px] mq750:leading-[25px]">
						{description}
					</div>
					<div className="  bg-primary-300 w-full max-w-[359.26px] h-[2.13px]"></div>
					<div className="flex  py-[18px] pb-[28px] justify-between items-center">
						{connected ? (
							<div className="cursor-pointer rounded-[2rem] text-[15px] font-[400] bg-background max-w-[136.05px] h-[42.52px] flex items-center justify-center w-full ">
								Disconnect
							</div>
						) : (
							<div className="cursor-pointer text-white rounded-[2rem] text-[15px] font-[400] bg-primary-300 max-w-[136.05px] gap-2  h-[42.52px] flex items-center justify-center w-full ">
								Connect
								<RefreshCcw />
							</div>
						)}
						<SlideSwitch on={connected} />
					</div>
				</div>
			) : (
				<div className="mq750:mx-[31.63px]  mq750:max-h-[300.95px] max-w-[407.48px] relative  bg-primary-300 bg-opacity-[0.2]  px-[23.5px] w-full max-h-[291.95px]  rounded-[2rem]">
					<div className="text-white left-[80.49px] mq750:left-[30px] whitespace-nowrap mq750:text-[30px] top-[119.95px] font-syne absolute font-[700] text-[30px]">
						Comming soon
					</div>
					<img
						className="w-[51px] h-[51px] mt-[10px]"
						src={image}
						alt=""
					/>
					<div className="w-full  font-[600] text-primary-300 text-[18px] ">
						{name}
					</div>
					<div className="w-full pt-[10px] mq750:pb-[15px] pb-[17px]  text-[15px]  font-[400px] leading-[28px] mq750:leading-[25px]">
						{description}
					</div>
					<div className="  bg-primary-300 w-full max-w-[359.26px] h-[2.13px]"></div>
					<div className="flex  py-[18px] pb-[28px] justify-between items-center">
						{connected ? (
							<div className="cursor-pointer rounded-[2rem] text-[15px] font-[400] bg-background max-w-[136.05px] h-[42.52px] flex items-center justify-center w-full ">
								Disconnect
							</div>
						) : (
							<div className="cursor-pointer text-white rounded-[2rem] text-[15px] font-[400] bg-primary-300 max-w-[136.05px] gap-2  h-[42.52px] flex items-center justify-center w-full ">
								Connect
								<RefreshCcw />
							</div>
						)}
						<SlideSwitch on={connected} />
					</div>
				</div>
			)}
		</>
	)
}

export default ChannelCard