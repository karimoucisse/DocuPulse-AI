import { IoSearchOutline } from "react-icons/io5";
import { MdAccountCircle } from "react-icons/md";
import Logo from "./Logo";

const Header = () => {
  return (
	<div className="flex w-screen justify-center py-4">
		<div className="flex items-center justify-between  max-w-6xl w-full bg-red">
			<Logo size="xl"/>
			<div className="flex gap-2 items-center">
				<label className="input rounded-xl">
					<IoSearchOutline/>
					<input type="search" placeholder="Rechercher des notebooks" className="input input-sm" />
				</label>
				<MdAccountCircle className="text-4xl"/>
			</div>
		</div>
	</div>
  )
}

export default Header
