import { styled } from "@mui/material/styles"
import FormGroup from "@mui/material/FormGroup"
import FormControlLabel from "@mui/material/FormControlLabel"
import Switch, { SwitchProps } from "@mui/material/Switch"

const Android12Switch = styled(Switch)(({ theme }) => ({
	padding: 8,
	"& .MuiSwitch-track": {
		borderRadius: 22 / 2,
		"&::before, &::after": {
			content: '""',
			position: "absolute",
			top: "50%",
			transform: "translateY(-50%)",
			width: 16,
			height: 16,
		}
	},
	"& .MuiSwitch-thumb": {
		boxShadow: "none",
		width: 16,
		height: 16,
		margin: 2,
	},
}))

export default function SlideSwitch() {
	return (
		<FormGroup>
			<FormControlLabel
				control={<Android12Switch defaultChecked />}
				label=""
			/>
		</FormGroup>
	)
}
