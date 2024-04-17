import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { BrowserRouter } from "react-router-dom";
import { CssBaseline, ThemeProvider, createTheme, StyledEngineProvider } from "@mui/material";
import { Theme } from "@radix-ui/themes";
import {Toaster} from 'sonner'
const muiTheme = createTheme();

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<BrowserRouter>
			<StyledEngineProvider injectFirst>
				<ThemeProvider theme={muiTheme}>
					<CssBaseline />
					<Theme>
						<App />
						<Toaster
                        position="bottom-right"
                        expand={true}
                        richColors
                        />
					</Theme>
				</ThemeProvider>
			</StyledEngineProvider>
		</BrowserRouter>
	</React.StrictMode>
)
