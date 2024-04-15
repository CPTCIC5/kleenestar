import * as React from "react"
import { Theme, useTheme } from "@mui/material/styles"
import Input from "@mui/material/Input"
import MenuItem from "@mui/material/MenuItem"
import FormControl from "@mui/material/FormControl"
import Select, { SelectChangeEvent } from "@mui/material/Select"
import InputLabel from "@mui/material/InputLabel"

const ITEM_HEIGHT = 48
const ITEM_PADDING_TOP = 8
const MenuProps = {
	PaperProps: {
		style: {
			maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
			width: 250,
		},
	},
}

function getStyles(name: string, personName: string[], theme: Theme) {
	return {
		fontWeight:
			personName.indexOf(name) === -1
				? theme.typography.fontWeightRegular
				: theme.typography.fontWeightMedium,
	}
}

type ops = {
	name: string
	value: string
}

function SelectOptions({
	options,
	InputText,
	...props
}: {
	options: Array<ops>
	InputText: string
}) {
	const isSmallScreen = window.innerWidth < 1000
	const theme = useTheme()
	const [personName, setPersonName] = React.useState<string>("")

	const handleChange = (event: SelectChangeEvent<typeof personName>) => {
		const {
			target: { value },
		} = event
		setPersonName(value)
	}

	return (
		<div className="w-full">
			<FormControl className="w-full">
				{!personName && (
					<InputLabel
						shrink={false}
						className="text-gray-500 focus:text-gray-500   border-transparent font-montserrat  text-[15px]">
						{InputText}
					</InputLabel>
				)}
				<Select
					labelId="demo-multiple-name-label"
					id="demo-multiple-name"
					value={personName}
					onChange={handleChange}
					input={
						personName ? (
							<Input
								{...props}
								disableUnderline
								className="w-full  bg-transparent min-h-[47px] h-full  border-transparent font-montserrat text-[15px]"
							/>
						) : (
							<Input
								{...props}
								disableUnderline
								className="w-full px-[10px]  bg-transparent  max-h-[47px] h-full  border-transparent font-montserrat text-[15px]"
							/>
						)
					}
					IconComponent={() => null} // This line hides the dropdown arrow
					MenuProps={MenuProps}>
					{options.map((option) => (
						<MenuItem
							key={option.name}
							value={option.value}
							style={{
								...getStyles(option.name, [personName], theme),
								fontFamily: "Montserrat",
								fontWeight: 400,
								fontSize: isSmallScreen ? "11px" : "14px",
								lineHeight: isSmallScreen ? "15px" : "17.07px",
							}}>
							{option.name}
						</MenuItem>
					))}
				</Select>
			</FormControl>
		</div>
	)
}

export default SelectOptions
