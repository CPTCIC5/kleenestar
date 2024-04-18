import {SquarePen} from 'lucide-react'


function ChatSideBar() {
  return (
		<aside className="bg-inherit  max-w-[375.93px] w-full h-full flex flex-col gap-[26.18px]">
			<div className="bg-white h-[86.91px] w-full flex items-center justify-between rounded-3xl px-[26.54px] py-[16.06px]">
				<div className="flex items-center justify-center gap-[18.13px]">
					<img
						className="w-[52.07px] h-[54.78px]"
						src="/group-672.svg"
						alt=""
					/>
					<span className="w-[156.02px] font-syne font-[700] text-[25px] leading-[30px]">
						Kleenestar
					</span>
				</div>
				<SquarePen  className="w-[20.94px] h-[20.94px] cursor-pointer" />
			</div>
			<div className="bg-white max-h-[580.12px] h-full w-full rounded-3xl"></div>
			<div className=" bg-white h-[124.61px] w-full rounded-3xl"></div>
		</aside>
	)
}

export default ChatSideBar