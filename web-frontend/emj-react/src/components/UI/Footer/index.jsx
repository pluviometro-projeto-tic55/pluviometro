import "./style.css";
import labclimaLogo from "../../../assets/labclima.png";

export default function Footer() {
  return (
    <footer className="footer mt-auto" role="contentinfo">
      <div className="footer-container">
        <span className="text-xs text-(--text-500) font-bold 3xl:text-base">
          © Colégio João XXIII — Liberdade para Transformar
        </span>

        <div className="footer-partner">
          <span className=" text-xs text-(--text-500) tracking-wide font-bold 3xl:text-base">
            PARCERIA TECNOLÓGICA
          </span>

          <img
            src={labclimaLogo}
            className="h-12.5 w-auto block 3xl:h-15"
            alt="Logo do parceiro LabClima"
          />
        </div>
      </div>
    </footer>
  );
}
