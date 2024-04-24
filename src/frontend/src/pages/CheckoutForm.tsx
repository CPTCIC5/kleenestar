
import {
	EmbeddedCheckoutProvider,
	EmbeddedCheckout,
} from "@stripe/react-stripe-js"
import { loadStripe } from "@stripe/stripe-js"
import axios from "axios"
import { useCallback } from "react"
import Cookies from 'js-cookie'


const CheckoutForm = () =>{
     const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_SECRET_KEY)
			const fetchClientSecret = useCallback(async () => {
				try {
					const response = await axios.post("/create-checkout-session",{
                        price: "69"
                    },{
                        withCredentials: true,
                        headers: {
                            'Content-Type': "application/json",
                            'X-CSRFToken': Cookies.get('csrftoken')
                        }
                    })
					return response.data.clientSecret
				} catch (error) {
					console.error("Error fetching client secret:", error)
					return null
				}
			}, [])
			const options = { fetchClientSecret }

    return (
			<div>
				<EmbeddedCheckoutProvider
					stripe={stripePromise}
					options={
                        
                        options}>
					<EmbeddedCheckout />
				</EmbeddedCheckoutProvider>
			</div>
		)
}

export default CheckoutForm